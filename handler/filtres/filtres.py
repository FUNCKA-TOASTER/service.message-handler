import re
import requests
import datetime
from db import db
from .base import BaseFilter


# ------------------------------------------------------------------------
class SlowModeQueueFilter(BaseFilter):
    NAME = "Slow mode queue"

    async def _handle(self, event: dict, kwargs) -> bool:
        if not self._is_anabled(event, "slow_mode", "system"):
            return False

        if self._user_in_queue(event):
            # TODO: Заменить на обращение к сервису наказаний.
            self._delete_own_message(event)
            return True

        interval = self._get_interval(event)
        query = f"""
        INSERT INTO 
            slow_mode_queue 
            (
                conv_id,
                user_id,
                user_name,
                prohibited_until
            )
        VALUES 
            (
                '{event.get("peer_id")}',
                '{event.get("user_id")}',
                '{event.get("user_name")}',
                NOW() + INTERVAL {interval} MINUTE
            );
        """

        db.execute.raw(schema="toaster", query=query)

        return True

    @staticmethod
    def _user_in_queue(event: dict) -> bool:
        user = db.execute.select(
            schema="toaster",
            table="slow_mode_queue",
            fields=("user_name",),
            conv_id=event.get("peer_id"),
            user_id=event.get("user_id"),
        )

        return bool(user)

    @staticmethod
    def _get_interval(event: dict) -> int:
        interval = db.execute.select(
            schema="toaster_settings",
            table="delay",
            fields=("delay",),
            conv_id=event.get("peer_id"),
            setting_name="slow_mode",
        )

        return int(interval[0][0]) if interval else 0


class OpenPMFilter(BaseFilter):
    NAME = "Open private messages"

    async def _handle(self, event: dict, kwargs) -> bool:
        if not self._is_anabled(event, "open_pm", "system"):
            return False

        can_write = self._get_write_status(event)

        if can_write:
            return False

        # TODO: Заменить на обращение к сервису наказаний.
        self._delete_own_message(event)
        return True

    def _get_write_status(self, event) -> bool:
        info = self.api.users.get(
            user_ids=event.get("user_id"), fields=["can_write_private_message"]
        )

        if not info:
            return True

        return bool(int(info[0].get("can_write_private_message")))


class AccountAgeFilter(BaseFilter):
    NAME = "Account Age"

    async def _handle(self, event: dict, kwargs) -> bool:
        if not self._is_anabled(event, "account_age", "system"):
            return False

        if not self._check_date(event):
            return False

        # TODO: Заменить на обращение к сервису наказаний.
        self._delete_own_message(event)
        return True

    def _check_date(self, event: dict) -> bool:
        pattern = r'<ya:created dc:date=".*"'

        response = requests.get(
            f"https://vk.com/foaf.php?id={event.get('user_id')}", timeout=50
        )
        found = re.findall(pattern, str(response.text))

        if not found:
            return False

        found = found[0][21:-1]
        found = found[found.find('"') + 1 :]
        found = found[: found.find('"')].replace("T", " ")
        found = found[: found.find("+")]

        created_at = datetime.datetime.strptime(found, "%Y-%m-%d %H:%M:%S")
        current_time = datetime.datetime.now()
        delta_seconds = (current_time - created_at).total_seconds()

        day_seconds = 60 * 60 * 24

        if delta_seconds < self._get_interval(event) * day_seconds:
            return True

        return False

    @staticmethod
    def _get_interval(event: dict) -> int:
        interval = db.execute.select(
            schema="toaster_settings",
            table="delay",
            fields=("delay",),
            conv_id=event.get("peer_id"),
            setting_name="account_age",
        )

        return int(interval[0][0]) if interval else 0


# TODO: доделать
class URLFilter(BaseFilter):
    NAME = "URL filter"

    async def _handle(self, event: dict, kwargs) -> bool:
        if not self._is_anabled(event, "url_filtering", "system"):
            return False

        hard_mode = self._is_anabled(event, "hard_url_filtering", "system")

        urls = self._get_urls(event.get("text").lower())
        domains = self._get_domains(urls)

        forbidden_domains = self._get_from_db(event, "domain", "forbidden")
        forbodden_urls = self._get_from_db(event, "url", "forbidden")

        if urls.intersection(forbodden_urls) or domains.intersection(forbidden_domains):
            # TODO: Заменить на обращение к сервису наказаний.
            self._delete_own_message(event)
            return True

        if hard_mode:
            allowed_domains = self._get_from_db(event, "domain", "allowed")
            allowed_urls = self._get_from_db(event, "url", "allowed")

            if urls - allowed_urls or domains - allowed_domains:
                # TODO: Заменить на обращение к сервису наказаний.
                self._delete_own_message(event)
                return True

        return False

    def _get_urls(self, text) -> set:
        pattern = r"(https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)?)"
        result = re.findall(pattern, text)
        return {url[0] for url in result}

    def _get_domains(self, url_list) -> set:
        pattern = r"(?<=://)(.*?)(?=\/)"
        return {re.findall(pattern, url)[0] for url in url_list}

    def _get_from_db(self, event, pattern_type, pattern_status) -> set:
        content = db.execute.select(
            schema="toaster_settings",
            table="url_filter",
            fields=("pattern",),
            conv_id=event.get("peer_id"),
            type=pattern_type,
            status=pattern_status,
        )

        return {c[0] for c in content}


class CurseWordsFilter(BaseFilter):
    NAME = "Curse words filter"

    async def _handle(self, event: dict, kwargs) -> bool:
        if not self._is_anabled(event, "curse_words", "system"):
            return False

        found = self._find_curse(event)

        if not found:
            return False

        # TODO: Заменить на обращение к сервису наказаний.
        self._delete_own_message(event)
        return True

    async def _find_curse(self, event) -> bool:
        word_list = db.execute.select(
            schema="toaster_settings",
            table="curse_words",
            fields=("word",),
            conv_id=event.get("peer_id"),
        )

        for word in word_list:
            pattern = rf"\b{word[0]}\b"
            return bool(re.findall(pattern, event.get("text").lower()))


# ------------------------------------------------------------------------
class ContentFilter(BaseFilter):
    NAME = "Content filter"
    CONTENT = (
        "app_action",
        "audio",
        "audio_message",
        "doc",
        "forward",
        "reply",
        "graffiti",
        "sticker",
        "link",
        "photo",
        "poll",
        "video",
        "wall",
    )

    async def _handle(self, event: dict, kwargs) -> bool:
        for content_name in self.CONTENT:
            if not self._is_anabled(event, content_name, "filter"):
                if self._has_content(event, content_name):
                    self.NAME = f"Content filter <{content_name}>"

                    # TODO: Заменить на обращение к сервису наказаний.
                    self._delete_own_message(event)
                    return True

        return False

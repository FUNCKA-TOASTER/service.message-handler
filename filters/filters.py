import re
import requests
from typing import Optional, NoReturn, Union, Set
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
from vk_api import VkApiError
from data import TOASTER_DB
from data import SettingStatus, UrlStatus, UrlType
from data.scripts import (
    get_user_queue_status,
    insert_user_to_queue,
    get_setting_delay,
    get_curse_words,
    get_patterns,
)
from toaster.broker.events import Event
from .base import BaseFilter
from loguru import logger


# ------------------------------------------------------------------------
class SlowModeQueue(BaseFilter):
    NAME = "Slow Mode"

    def _handle(self, event: Event) -> bool:
        setting = "slow_mode"
        status = self._is_setting_enabled(event, setting)
        if status == SettingStatus.inactive:
            return False

        expired = get_user_queue_status(
            db_instance=TOASTER_DB,
            uuid=event.user.uuid,
            bpid=event.peer.bpid,
        )

        if expired is not None:
            comment = "Помедленнее! Соблюдай интервал сообщений."
            self._publish_punishment(
                type="warn",
                comment=comment,
                setting=setting,
                event=event,
            )
            return True

        insert_user_to_queue(
            db_instance=TOASTER_DB,
            uuid=event.user.uuid,
            bpid=event.peer.bpid,
            setting=setting,
        )

        return False


class OpenPrivateMessages(BaseFilter):
    NAME = "Open Private Messages"

    def _handle(self, event: Event) -> bool:
        setting = "open_pm"
        status = self._is_setting_enabled(event, setting)
        if status == SettingStatus.inactive:
            return False

        is_opened = self._get_pm_status(event)

        if not is_opened:
            comment = "Необходимо открыть личные сообщения."
            self._publish_punishment(
                type="warn",
                comment=comment,
                setting=setting,
                event=event,
            )
            return True

        return False

    def _get_pm_status(self, event: Event) -> Union[bool, NoReturn]:
        try:
            self.api.users.get(
                user_ids=event.user.uuid,
                fields=["can_write_private_message"],
            )[0].get("can_write_private_message")

        except VkApiError as e:
            raise RuntimeError(f"Error getting PM status: {e}")


class AccountAge(BaseFilter):
    NAME = "Account Age"

    def _handle(self, event: Event) -> bool:
        setting = "account_age"
        status = self._is_setting_enabled(event, setting)
        if status == SettingStatus.inactive:
            return False

        url = f"https://vk.com/foaf.php?id={event.user.uuid}"
        str_xml_data = self.fetch_and_parse_xml(url)

        if str_xml_data:
            created_date = self.extract_created_date(str_xml_data)
            if created_date:
                interval = get_setting_delay(
                    db_instance=TOASTER_DB,
                    name=setting,
                    bpid=event.peer.bpid,
                )
                delta = timedelta(days=interval)
                current_date = datetime.now()

                if (current_date - created_date) < delta:
                    comment = "Ваш аккаунт слишком молод."
                    self._publish_punishment(
                        type="warn",
                        comment=comment,
                        setting=setting,
                        event=event,
                    )
                    return True

        return False

    @staticmethod
    def fetch_and_parse_xml(url: str) -> Optional[str]:
        try:
            response = requests.get(url, timeout=50)
            response.raise_for_status()
            logger.debug(response.text)
            return response.text

        except requests.RequestException as e:
            raise RuntimeError(f"Error fetching XML: {e}")

    @staticmethod
    def extract_created_date(str_xml_data: str) -> Optional[Union[datetime, NoReturn]]:
        try:
            root = ET.fromstring(str_xml_data)
            namespaces = {
                "ya": "http://blogs.yandex.ru/schema/foaf/",
                "dc": "http://purl.org/dc/elements/1.1/",
            }

            created_element = root.find(".//ya:created", namespaces)
            logger.debug(created_element)
            logger.debug(created_element.attrib)
            if created_element is not None and "dc:date" in created_element.attrib:
                created_date_str = created_element.attrib["dc:date"]
                return datetime.fromisoformat(created_date_str)

            else:
                raise RuntimeError("Created date not found in the XML.")

        except ET.ParseError as e:
            raise RuntimeError(f"Error parsing XML: {e}")


class LinksAndDomains(BaseFilter):
    NAME = "Links & Domains"

    def _handle(self, event: Event) -> bool:
        setting = "url_filtering"
        status = self._is_setting_enabled(event, setting)
        if status == SettingStatus.inactive:
            return False

        text = event.message.text.lower()
        text_links = self._get_links(text=text)

        forbidden_links, forbidden_domains, allowed_links, allowed_domains = (
            self._get_patterns(event=event, setting=setting)
        )

        hard_mode = self._is_setting_enabled(event, "hard_url_filtering")
        for link in text_links:
            domain = self._get_domain(link)
            if {domain} & forbidden_domains:
                if {link} & allowed_links:
                    if hard_mode:
                        self._init_publish(event=event, setting="hard_url_filtering")
                        self.NAME = self.NAME + " <grey link>"
                        return True

                else:
                    self._init_publish(event=event, setting=setting)
                    self.NAME = self.NAME + " <forbidden domain>"
                    return True

            if {link} & forbidden_links:
                self._init_publish(event=event, setting=setting)
                self.NAME = self.NAME + " <forbidden link>"
                return True

            if not {domain} & allowed_domains and hard_mode:
                self._init_publish(event=event, setting="hard_url_filtering")
                self.NAME = self.NAME + " <grey domain>"
                return True

        return False

    @staticmethod
    def _get_links(text: str) -> set:
        pattern = r"(https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)?)"
        result = re.findall(pattern, text)
        return {url[0] for url in result}

    @staticmethod
    def _get_domain(link: str) -> Optional[set]:
        pattern = r"(?<=://)(.*?)(?=\/)"
        domain = re.findall(pattern, link)
        return domain[0] if domain else None

    def _init_publish(self, event: Event, setting: str):
        comment = "Эту ссылку\домен запрещено распространять."
        self._publish_punishment(
            type="warn",
            comment=comment,
            setting=setting,
            event=event,
        )

    def _get_patterns(self, event: Event) -> Set[str]:
        properties = [
            (UrlType.url, UrlStatus.forbidden),
            (UrlType.domain, UrlStatus.forbidden),
            (UrlType.url, UrlStatus.allowed),
            (UrlType.domain, UrlStatus.allowed),
        ]

        result = []
        for type, status in properties:
            result.append(
                get_patterns(
                    db_instance=TOASTER_DB,
                    bpid=event.peer.bpid,
                    type=type,
                    status=status,
                )
            )

        return result


class CurseWords(BaseFilter):
    NAME = "Curse Words"

    def _handle(self, event: Event) -> bool:
        setting = "curse_words"
        status = self._is_setting_enabled(event, setting)
        if status == SettingStatus.inactive:
            return False

        word_list = get_curse_words(
            db_instance=TOASTER_DB,
            bpid=event.peer.bpid,
        )

        for word in word_list:
            text = event.message.text.lower()
            if re.search(r"\b" + re.escape(word) + r"\b", text):
                comment = "Это слово запрещено."
                self._publish_punishment(
                    type="warn",
                    comment=comment,
                    setting=setting,
                    event=event,
                )
                return True

        return False


class Content(BaseFilter):
    NAME = "Content"
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
        "geo",
    )

    def _handle(self, event: Event) -> bool:
        for setting in self.CONTENT:
            if not self._is_setting_enabled(event, setting):
                if self._has_content(event, setting):
                    self.NAME = self.NAME + f" <{setting}>"

                    comment = "Этот контент запрещен."
                    self._publish_punishment(
                        type="warn",
                        comment=comment,
                        setting=setting,
                        event=event,
                    )
                    return True

        return False

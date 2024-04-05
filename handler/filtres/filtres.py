from db import db
from .base import BaseFilter



# ------------------------------------------------------------------------
class SlowModeQueueFilter(BaseFilter):
    """Slow mode filter system
    """
    NAME = "Slow mode queue"

    # TODO: Добавить игнор для модерации\администрации\персонала.
    async def _handle(self, event: dict, kwargs) -> bool:
        if not self._is_anabled(event, "slow_mode", "system"):
            return False

        if self._user_in_queue(event):
            #TODO: Выдать наказание

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

        db.execute.raw(
            schema="toaster",
            query=query
        )

        return True


    @staticmethod
    def _user_in_queue(event: dict) -> bool:
        user = db.execute.select(
            schema="toaster",
            table="slow_mode_queue",
            fields=("user_name",),
            conv_id=event.get("peer_id"),
            user_id=event.get("user_id")
        )

        return bool(user)


    @staticmethod
    def _get_interval(event: dict) -> int:
        interval = db.execute.select(
            schema="toaster_settings",
            table="slow_mode_delay",
            fields=("delay",),
            conv_id=event.get("peer_id")
        )

        return int(interval[0][0]) if interval else 0



class OpenPMFilter(BaseFilter):
    """Slow mode filter system
    """
    NAME = "Open private messages"

    # TODO: Добавить игнор для модерации\администрации\персонала.
    async def _handle(self, event: dict, kwargs) -> bool:
        if not self._is_anabled(event, "open_pm", "system"):
            return False

        can_write = self._get_write_status(event)

        if can_write:
            return True

        #TODO: Выдать наказание

        self._delete_own_message(event)
        return True


    def _get_write_status(self, event) -> bool:
        info = self.api.users.get(
            event.get("user_id"),
            fields=["can_write_private_message"]
        )

        if not info:
            return True

        return bool(info[0].get("can_write_private_message"))

# ------------------------------------------------------------------------
class ContentFilter(BaseFilter):
    """Message content filering
    """
    NAME = "Content filter"
    CONTENT = (
        "app_action", "audio",
        "audio_message", "doc",
        "forward", "reply",
        "graffiti", "sticker",
        "link", "photo",
        "poll", "video",
        "wall"
    )

    # TODO: Добавить игнор для модерации\администрации\персонала.
    async def _handle(self, event: dict, kwargs) -> bool:
        for content_name in self.CONTENT:
            if not self._is_anabled(event, content_name, "filter"):
                if self._has_content(event, content_name):
                    self.NAME = f"Content filter <{content_name}>"
                    #TODO: Выдать наказание

                    self._delete_own_message(event)
                    return True

        return False

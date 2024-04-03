from vk_api import VkApiError
from db import db
from .base import BaseFilter



# ------------------------------------------------------------------------
class SlowModeQueueFilter(BaseFilter):
    """Slow mode filter system
    """
    NAME = "Slow mode queue"

    # TODO: Добавить инор для модерации\администрации\персонала.
    async def _handle(self, event: dict, kwargs) -> bool:
        if not self._is_anabled(event, "system_status", "Slow_mode"):
            return False

        if self._user_in_queue(event):
            #TODO: Выдать наказание

            self.delete_own_message(event)
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



# ------------------------------------------------------------------------
class ContentFilter(BaseFilter):
    """Slow mode filter system
    """
    NAME = "Content filter"
    CONTENT = (
        "App_action", "Audio",
        "Audio_message", "Doc",
        "Forward", "Reply",
        "Graffiti", "Sticker",
        "Link", "Photo",
        "Poll", "Video",
        "Wall"
    )

    # TODO: Добавить инор для модерации\администрации\персонала.
    async def _handle(self, event: dict, kwargs) -> bool:
        for content_name in self.CONTENT:
            if self._is_anabled(event, "filter_status", content_name):
                if self._has_content(event, content_name.lower()):
                    self.NAME = f"Content filter <{content_name}>"
                    #TODO: Выдать наказание

                    self.delete_own_message(event)
                    return True

        return False

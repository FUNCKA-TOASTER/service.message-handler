from vk_api import VkApiError
from db import db
from .base import BaseFilter



# ------------------------------------------------------------------------
class SlowModeQueueFilter(BaseFilter):
    """Slow mode filter system
    """
    NAME = "Slow mode queue"

    async def _handle(self, event: dict, kwargs) -> bool:
        if not self._is_anabled(event):
            return False

        if self._user_in_queue(event):
            #TODO: Выдать наказание

            try:
                self.api.messages.delete(
                    delete_for_all=1,
                    peer_id=event.get("peer_id"),
                    cmids=event.get("cmid")
                )

            except VkApiError:
                ...

            return True

        #TODO: Апдейт при конфликте
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
    def _is_anabled(event: dict) -> bool:
        setting = db.execute.select(
            schema="toaster_settings",
            table="system_status",
            fields=("system_status",),
            conv_id=event.get("peer_id"),
            system_name="Slow_mode"
        )

        return bool(setting[0][0]) if setting else False


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

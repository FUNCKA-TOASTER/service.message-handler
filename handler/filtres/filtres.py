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
            # Выдать наказание
            return True


        interval = self._get_interval(event)
        db.execute.insert(
            schema="toaster",
            table="slow_mode_queue",
            on_duplicate=None,
            conv_id=event.get("peer_id"),
            user_id=event.get("user_id"),
            user_name=event.get("user_name"),
            prohibited_until=f"NOW() + INTERVAL {interval} MINUTE AS PUT"
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

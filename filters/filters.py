from data import TOASTER_DB
from data import SettingStatus
from data.scripts import (
    get_user_queue_status,
    insert_user_to_queue,
)
from toaster.broker.events import Event
from .base import BaseFilter


# ------------------------------------------------------------------------
class SlowModeQueue(BaseFilter):
    NAME = "Slow Mode"

    def _handle(self, event: Event) -> bool:
        from loguru import logger

        setting = "slow_mode"
        status = self._is_setting_enabled(event, setting)
        if status == SettingStatus.inactive:
            return False

        logger.debug(1)

        expired = get_user_queue_status(
            db_instance=TOASTER_DB,
            uuid=event.user.uuid,
            bpid=event.peer.bpid,
        )

        if expired is not None:
            # get_setting_points()
            # TODO: Запустить действие в сервисе наказаний.
            # На сервис наказаний отправить:
            #   - type: "warn"                       (Название действия)
            #   - uuid: target_id                    (ID нарушителя)
            #   - points: points                     (Кол-во варнов)
            #   - bpid: event.peer.bpid              (Где произошло)
            #   - cmids: [event.message.reply.cmid]  (Если есть - удалить это сообщение)

            return True

        logger.debug(2)

        insert_user_to_queue(
            db_instance=TOASTER_DB,
            uuid=event.user.uuid,
            bpid=event.peer.bpid,
            setting=setting,
        )

        logger.debug(3)

        return False

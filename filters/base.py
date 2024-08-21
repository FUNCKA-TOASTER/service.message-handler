"""Module "filters".

File:
    base.py

About:
    File describing base bot filter class.
"""

from abc import ABC, abstractmethod
from vk_api import VkApi
from db import TOASTER_DB
from toaster.enums import SettingStatus
from toaster.scripts import (
    get_setting_status,
    get_setting_points,
)
from funcka_bots.broker.events import (
    Event,
    Punishment,
)
from funcka_bots.broker import (
    Publisher,
    build_connection,
)
import config


class BaseFilter(ABC):
    """Base class of the bot filter."""

    NAME = "None"
    publisher = Publisher(build_connection(config.REDIS_CREDS))

    def __init__(self, api: VkApi) -> None:
        self.api = api

    def __call__(self, event: Event) -> bool:
        return self._handle(event)

    @abstractmethod
    def _handle(self, event: Event) -> bool:
        """The main function of filter execution.

        Args:
            event (Event): Custom Event object.

        Returns:
            bool: Execution status.
        """

    @staticmethod
    def _is_setting_enabled(event: Event, name: str) -> bool:
        status = get_setting_status(
            db_instance=TOASTER_DB,
            bpid=event.peer.bpid,
            name=name,
        )
        return status == SettingStatus.active

    @staticmethod
    def _has_content(event: Event, content_name: str) -> bool:
        attachments = event.message.attachments
        return content_name in attachments

    def _publish_punishment(
        self, type: str, comment: str, setting: str, event: Event
    ) -> None:
        coeff = 1
        if type == "unwarn":
            type = "warn"
            coeff = -1
        punishment = Punishment(type=type, comment=comment)
        punishment.set_cmids(cmids=event.message.cmid)
        punishment.set_target(bpid=event.peer.bpid, uuid=event.user.uuid)
        if type == "warn":
            points = get_setting_points(
                db_instance=TOASTER_DB,
                bpid=event.peer.bpid,
                name=setting,
            )
            punishment.set_points(points=points * coeff)
        self.publisher.publish(punishment, "punishment")

"""Module "filters".

File:
    base.py

About:
    File describing base bot filter class.
"""

from abc import ABC, abstractmethod
from vk_api import VkApi
from funcka_bots.events import BaseEvent, event_builder
from funcka_bots.broker import Publisher
from toaster.enums import SettingStatus
from toaster.scripts import (
    get_setting_status,
    get_setting_points,
)
import config


class BaseFilter(ABC):
    """Base class of the bot filter."""

    NAME = "None"
    publisher = Publisher(creds=config.BROKER_CREDS)

    def __init__(self, api: VkApi) -> None:
        self.api = api

    def __call__(self, event: BaseEvent) -> bool:
        return self._handle(event)

    @abstractmethod
    def _handle(self, event: BaseEvent) -> bool:
        """The main function of filter execution.

        Args:
            event (Event): Custom Event object.

        Returns:
            bool: Execution status.
        """

    @staticmethod
    def _is_setting_enabled(event: BaseEvent, name: str) -> bool:
        status = get_setting_status(
            bpid=event.peer.bpid,
            name=name,
        )
        return status == SettingStatus.active

    @staticmethod
    def _has_content(event: BaseEvent, content_name: str) -> bool:
        attachments = event.message.attachments
        return content_name in attachments

    def _publish_punishment(
        self,
        punishment_type: str,
        punishment_comment: str,
        setting: str,
        event: BaseEvent,
    ) -> None:
        if punishment_type in ("warn", "unwarn"):
            points = get_setting_points(
                bpid=event.peer.bpid,
                name=setting,
            )

        punishment = event_builder.build_punishment(
            punishment_type=punishment_type,
            punishment_comment=punishment_comment,
            peer=dict(event.peer._asdict()),
            user=dict(event.user._asdict()),
            message={"cmid": event.message.cmid, "text": "", "attachments": []},
            warn={"points": points} if punishment_type == "warn" else None,
            unwarn={"points": points * -1} if punishment_type == "unwarn" else None,
            kick={"mode": "local"} if punishment_type == "kick" else None,
        )

        self.publisher.publish(punishment, "punishment")

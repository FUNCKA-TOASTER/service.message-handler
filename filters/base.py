"""Module "filters".

File:
    base.py

About:
    File describing base bot filter class.
"""

from abc import ABC, abstractmethod
from vk_api import VkApi
from data import TOASTER_DB
from data.scripts import get_setting_status
from toaster.broker.events import Event


class BaseFilter(ABC):
    """Base class of the bot filter."""

    NAME = "None"

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
        enabled = get_setting_status(
            db_instance=TOASTER_DB,
            bpid=event.peer.bpid,
            name=name,
        )
        return enabled

    @staticmethod
    def _has_content(event: Event, content_name: str) -> bool:
        attachments = event.message.attachments
        return content_name in attachments

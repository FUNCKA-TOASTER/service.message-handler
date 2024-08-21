"""Module "handler".

File:
    handler.py

About:
    File describing message handler class.
"""

import json
from typing import (
    Any,
    Optional,
    NoReturn,
)
from loguru import logger
from vk_api import VkApi
from funcka_bots.broker.events import Event
from funcka_bots.handler import ABCHandler
from db import TOASTER_DB
from toaster.enums import UserPermission
from toaster.scripts import (
    get_log_peers,
    get_user_permission,
)
from filters import filter_list
import config


class MessageHandler(ABCHandler):
    """Message handler class."""

    def __call__(self, event: Event) -> None:
        try:
            self._check_permissions(event)
            self._check_content(event)

            if response := self._execute(event):
                log, filter = response
                logger.info(log)
                self._alert_about_execution(event, filter)
                return

        except Exception as error:
            logger.error(error)

        else:
            logger.info("Not a single filter was triggered.")

    def _execute(self, event: Event) -> Optional[str]:
        for selected in filter_list:
            filter_obj = selected(self._get_api())
            if filter_obj(event):
                filter = filter_obj.NAME
                return (f"Filter '{filter}' was triggered.", filter)

    @staticmethod
    def _check_content(event: Event) -> Optional[NoReturn]:
        content = (
            event.message.text,
            event.message.attachments,
            "reply" in event.message.attachments,
            "forwars" in event.message.attachments,
        )
        if not any(content):
            raise AttributeError("Missing message content.")

    @staticmethod
    def _check_permissions(event: Event) -> Optional[NoReturn]:
        permission = get_user_permission(
            db_instance=TOASTER_DB,
            uuid=event.user.uuid,
            bpid=event.peer.bpid,
        )

        if permission != UserPermission.user:
            raise PermissionError("Ignoring filtering for staff messages.")

    def _alert_about_execution(self, event: Event, name: str):
        answer_text = (
            f"[id{event.user.uuid}|{event.user.name}] не прошел проверку. \n"
            f"Беседа: {event.peer.name} \n"
            f"Фильтр: {name} \n"
        )

        forward = {
            "peer_id": event.peer.bpid,
            "conversation_message_ids": [event.message.cmid],
        }

        api = self._get_api()

        for bpid in get_log_peers(db_instance=TOASTER_DB):
            api.messages.send(
                peer_ids=bpid,
                random_id=0,
                message=answer_text,
                forward=json.dumps(forward),
            )

    def _get_api(self) -> Any:
        session = VkApi(
            token=config.TOKEN,
            api_version=config.API_VERSION,
        )
        return session.get_api()

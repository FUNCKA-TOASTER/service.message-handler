from logger import logger
from db import db
from .abc import ABCHandler
from .filtres import filter_list


class MessageHandler(ABCHandler):
    async def _handle(self, event: dict, kwargs) -> bool:
        if await self._get_userlvl(event) > 0:
            log_text = "Ignoring messages from staff."
            await logger.info(log_text)

            return False

        if not any(
            (
                event.get("text", False),
                event.get("attachments", False),
                event.get("reply", False),
                event.get("forward", False),
            )
        ):
            log_text = f"Missing message content <{event.get('event_id')}>"
            await logger.info(log_text)

            return False

        log_text = f"Event <{event.get('event_id')}> "

        for filt in filter_list:
            selected = filt(super().api)
            result = await selected(event)
            if result:
                log_text += f'triggered "{selected.NAME}" filter.'
                await logger.info(log_text)
                return result

        log_text += "did not triggered any filter."

        await logger.info(log_text)
        return False

    async def _get_userlvl(self, event: dict) -> int:
        tech_admin = db.execute.select(
            schema="toaster_settings",
            table="staff",
            fields=("user_id",),
            user_id=event.get("user_id"),
            staff_role="TECH",
        )

        if bool(tech_admin):
            if event.get("user_id") == tech_admin[0][0]:
                return 2

        user_lvl = db.execute.select(
            schema="toaster",
            table="permissions",
            fields=("user_permission",),
            conv_id=event.get("peer_id"),
            user_id=event.get("user_id"),
        )

        if bool(user_lvl):
            return int(user_lvl[0][0])

        return 0


message_handler = MessageHandler()

from logger import logger
from .abc import ABCHandler
from .filtres import (
    text_filter_list,
    attachments_filter_list,
    reply_filter_list
)


class MessageHandler(ABCHandler):
    """Event handler class that recognizes commands
    in the message and executing attached to each command
    actions.
    """
    async def _handle(self, event: dict, kwargs) -> bool:
        if not any((
            event.get("text", False),
            event.get("attachments", False),
            event.get("reply", False),
            event.get("forward", False)
        )):
            log_text = f"Missing message content <{event.get('event_id')}>"
            await logger.info(log_text)

            return False

        log_text = f"Event <{event.get('event_id')}> "

        # TODO: Try to rework
        if event.get("text", False):
            for text_filter in text_filter_list:
                selected = text_filter(super().api)
                result = await selected(event)
                if result:
                    log_text += f"triggered \"{selected.NAME}\" filter."
                    await logger.info(log_text)
                    return result

        if event.get("attachments", False):
            for attachment_filter in attachments_filter_list:
                selected = attachment_filter(super().api)
                result = await selected(event)
                if result:
                    log_text += f"triggered \"{selected.NAME}\" filter."
                    await logger.info(log_text)
                    return result

        if event.get("reply", False) or event.get("forward", False):
            for reply_filter in reply_filter_list:
                selected = reply_filter(super().api)
                result = await selected(event)
                if result:
                    log_text += f"triggered \"{selected.NAME}\" filter."
                    await logger.info(log_text)
                    return result

        log_text += "did not triggered any action."

        await logger.info(log_text)
        return False



message_handler = MessageHandler()

from vk_api import VkApi
from tools.keyboards import SnackbarAnswer
from .abc import ABCHandler


class BaseFilter(ABCHandler):
    """Command handler base class.
    """
    NAME = "None"

    def __init__(self, api: VkApi):
        self.api = api


    def snackbar(self, event: dict, text: str):
        """Sends a snackbar to the user.

        Args:
            event (ButtonEvent): VK button_pressed custom event.
            text (str): Sncakbar text.
        """
        self.api.messages.sendMessageEventAnswer(
            event_id=event.get("button_event_id"),
            user_id=event.get("user_id"),
            peer_id=event.get("peer_id"),
            event_data=SnackbarAnswer(text).data
        )


    async def log(self):
        """Sends a log of command execution
        in log-convs.
        """
        # TODO: write me

"""Module "keyboards".

File:
    button.py

About:
    File describing the VK keyboard button class.
"""

from typing import Dict, Union
from .action import BaseAction
from .color import ButtonColor

Payload = Dict[str, Union[str, int]]


class Button:
    """VK keyboard button class."""

    def __init__(self, action: BaseAction, color: ButtonColor, owner_id: int):
        self.action = action
        self.color = color
        self.owner_id = owner_id

    @property
    def data(self) -> Payload:
        """Returns the data of the button as a dictionary.

        Returns:
            dict: Button dictionary repr.
        """
        self.action.payload.setdefault("keyboard_owner", self.owner_id)

        data = {"action": self.action.data, "color": self.color.value}

        return data

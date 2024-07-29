"""Module "keyboards".

File:
    keyboard.py

About:
   File describing VK keyboard builder class.
"""

import json
from typing import Any, Dict, Union
from .button import Button
from .action import BaseAction
from .color import ButtonColor

Payload = Dict[str, Union[str, int]]


class Keyboard:
    """VK keyboard builder class."""

    def __init__(self, inline: bool, one_time: bool, owner_id: int):
        self.owner_id = owner_id
        self.inline: bool = inline
        self.one_time: bool = one_time
        self.buttons: list = []

    def add_row(self) -> Any:
        """Adds a new line for placing buttons.
        The count of lines cannot exceed 6.

        Raises:
            ValueError: The maximum count of rows has been exceeded.
            RuntimeError: Cannot create a new row while the previous row is empty.

        Returns:
            Any: self
        """
        if len(self.buttons) > 6:
            raise ValueError("The maximum count of rows has been exceeded.")

        if self.buttons and not self.buttons[-1]:
            raise RuntimeError(
                "Cannot create a new row while the previous row is empty."
            )

        self.buttons.append([])

        return self

    def add_button(self, action: BaseAction, color: ButtonColor) -> Any:
        """Adds a new button to the last row created.

        Args:
            action (BaseAction): VK keyboard button action.
            color (ButtonColor): VK keyboard button color.

        Raises:
            RuntimeError: Missing button rows.

        Returns:
            Any: self.
        """
        if not self.buttons:
            raise RuntimeError("Missing button rows.")

        new_button = Button(action, color, self.owner_id).data
        self.buttons[-1].append(new_button)

        return self

    @property
    def as_dict(self) -> Payload:
        """Returns the data of the keyboard as a dictionary.

        Returns:
            Payload: Keyboard data dictionary repr.
        """
        body = {
            "one_time": self.one_time,
            "inline": self.inline,
            "buttons": self.buttons,
        }

        return body

    @property
    def json(self) -> str:
        """Converts keyboard object fields to JSON string.

        Returns:
            str: JSON dumped string.
        """
        return json.dumps(self.as_dict)

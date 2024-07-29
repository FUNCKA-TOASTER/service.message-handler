"""Module "keyboards".

File:
    answer.py

About:
    File describing the answers classes of VK keyboard buttons.
"""

import json
from typing import Dict, Union

Payload = Dict[str, Union[str, int]]


class BaseAnswer:
    """VK keyboard button action base class."""

    def __init__(self, action_type: str):
        self.type = action_type

    @property
    def data(self) -> Payload:
        """Returns a dictionary representation of the button
        answer feilds.

        Returns:
            dict: Answer dictionary repr.
        """
        data = {key: value for key, value in vars(self).items()}

        return json.dumps(data)


class SnackbarAnswer(BaseAnswer):
    """Send a snackbar as response."""

    def __init__(self, text: str):
        super().__init__("show_snackbar")

        self.text = text


class LinkAnswer(BaseAnswer):
    """Follow a link as response."""

    def __init__(self, url: str):
        super().__init__("open_link")

        self.link = url


class AppAnswer(BaseAnswer):
    """Open VK Mini App as response."""

    def __init__(self, app_hash: str, app_id: int, owner_id: int):
        super().__init__("open_app")

        self.hash = app_hash
        self.app_id = app_id
        self.owner_id = owner_id

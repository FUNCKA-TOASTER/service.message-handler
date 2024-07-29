"""Module "keyboards".

File:
    action.py

About:
    File describing button action classes VK keyboards.
"""

from typing import Dict, Union

Payload = Dict[str, Union[str, int]]


class BaseAction:
    """VK keyboard button action base class."""

    def __init__(self, action_type: str):
        self.type = action_type

    @property
    def data(self) -> Payload:
        """Returns a dictionary representation of the
        button action feilds.

        Returns:
            dict: Action dictionary representation.
        """
        data = {key: value for key, value in vars(self).items()}

        return data


class Text(BaseAction):
    """Sends the text of the clicked button to the dialog."""

    def __init__(self, label: str, payload: Payload):
        super().__init__("text")

        self.label = label
        self.payload = payload


class OpenLink(BaseAction):
    """Follows a link."""

    def __init__(self, url: str, label: str, payload: Payload):
        super().__init__("open_link")

        self.link = url
        self.label = label
        self.payload = payload


class Location(BaseAction):
    """Sends geolocation to the dialog."""

    def __init__(self, url: str, label: str, payload: Payload):
        super().__init__("location")

        self.link = url
        self.label = label
        self.payload = payload


class VKPay(BaseAction):
    """Opens the VKPay payment window."""

    def __init__(self, payment_hash: str, label: str, payload: Payload):
        super().__init__("vkpay")

        self.hash = payment_hash
        self.label = label
        self.payload = payload


class OpenApp(BaseAction):
    """Opens the VK Mini App."""

    def __init__(
        self,
        app_hash: str,
        label: str,
        app_id: int,
        owner_id: int,
        payload: Payload,
    ):
        super().__init__("open_app")

        self.hash = app_hash
        self.label = label
        self.payload = payload
        self.app_id = app_id
        self.owner_id = owner_id


class Callback(BaseAction):
    """Sends a click notification to the server."""

    def __init__(self, label: str, payload: Payload):
        super().__init__("callback")

        self.label = label
        self.payload = payload

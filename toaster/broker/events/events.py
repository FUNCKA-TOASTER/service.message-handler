"""Module "events".

File:
    events.py

About:
    File describing custom Event class.
"""

from typing import Dict, Union, Optional, Any, List
from abc import ABC, abstractmethod


Payload = Dict[str, Union[str, int]]


class BaseEvent(ABC):
    @abstractmethod
    def __str__(self) -> str:
        pass

    def __repr__(self) -> str:
        return self.__str__()

    def as_dict(self) -> Payload:
        """Converts the BaseEvent object to a dictionary.

        Description:
            This method is used only for logging
            purposes and is not intended for future
            data exchange.

        Returns:
            dict: Dictionary representation.
        """

        dict_repr = {}
        for attr, value in vars(self).items():
            if not callable(value) and not attr.startswith("__"):
                if isinstance(value, tuple):
                    dict_repr[attr] = value._asdict()
                else:
                    dict_repr[attr] = value

        return dict_repr


class Event(BaseEvent):
    """Class for representing an event.

    Attributes:
        event_id (str): Unique identifier for the event.
        event_type (str): Type of the event.

    ---OPTIONAL---
    Dynamically defined attributes:
        Always determined:
            user (User): Data of the user who called the event.
            peer (Peer): Data of the peer where the event occurred.

        Determined depending on the type of event:
            button (Button): Button click data.
            reaction (Reaction): Reaction data for the message.
            message (Message): Message data.
    """

    event_id: str = None
    event_type: str = None

    def __init__(self, raw_event: Payload, type: str = "Undefined"):
        """Initializes an Event object.

        Args:
            raw_event (dict): Raw dictionary containing event data.
            type (str): Type of the event (default is "Undefined").
        """

        self.event_type = type
        self.event_id = raw_event.get("event_id")

    def __str__(self) -> str:
        string = (
            "<-- "
            f"class Event <type: {self.event_type}>"
            " | "
            f"<id: {self.event_id}>"
            " -->"
        )
        return string

    def add_object(self, name: str, value: Any) -> None:
        """Добавляет обьект данных события в качестве атрибута класса.

        Args:
            name (str): Object name.
            value (Any): Object value.
        """

        self.__setattr__(name, value)


class Punishment(BaseEvent):
    """DOCSTRING"""

    punishment_type: str = None

    def __init__(self, type: str = "Undefined", comment: Optional[str] = None) -> None:
        self.punishment_type = type
        self.comment = comment

    def __str__(self) -> str:
        string = (
            "<-- "
            f"class Punishment <type: {self.punishment_type}>"
            " | "
            f"<comment: {self.event_id}>"
            " -->"
        )
        return string

    def set_cmids(self, cmids: Union[int, List[int]]) -> None:
        if isinstance(cmids, list):
            self.cmids = [cmid for cmid in cmids]
        elif isinstance(cmids, int):
            self.cmids = [cmids]
        else:
            raise TypeError("cmids argument must be 'int' or 'list of int'")

    def set_target(self, bpid: int, uuid: int) -> None:
        self.bpid = bpid
        self.uuid = uuid

    def set_points(self, points: int) -> None:
        if self.punishment_type == "warn":
            self.points = points
        else:
            raise TypeError("Cannot set points to a punishment not a warn type.")

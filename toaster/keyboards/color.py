"""Module "keyboards".

File:
    color.py

About:
   File describing enumerate of button colors.
"""

from enum import Enum


class ButtonColor(Enum):
    """Button color enumerate class.

    Attributes:
        PRIMARY
        SECONDARY
        POSITIVE
        NEGATIVE
    """

    PRIMARY = "primary"
    SECONDARY = "secondary"
    POSITIVE = "positive"
    NEGATIVE = "negative"

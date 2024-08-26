"""Module "config".

File:
    __init__.py

About:
    Initializing the "config" module.
"""

from .config import (
    BROKER_CREDS,
    BROKER_QUEUE_NAME,
    VK_GROUP_TOKEN,
    VK_GROUP_ID,
    VK_API_VERSION,
)


__all__ = (
    "BROKER_CREDS",
    "BROKER_QUEUE_NAME",
    "VK_GROUP_TOKEN",
    "VK_GROUP_ID",
    "VK_API_VERSION",
)

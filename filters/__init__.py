"""Module "filters".

File:
    __init__.py

About:
    Initializing the "filters" module.
"""

from .filters import (
    SlowModeQueue,
    OpenPrivateMessages,
    AccountAge,
    CurseWords,
    Content,
    LinksAndDomains,
)

# Filters in order of priority of execution
filter_list = [
    AccountAge,
    OpenPrivateMessages,
    Content,
    LinksAndDomains,
    CurseWords,
    SlowModeQueue,
]


__all__ = ("filter_list",)

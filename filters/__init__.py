"""Module "filters".

File:
    __init__.py

About:
    Initializing the "filters" module.
"""

from .filters import (
    SlowModeQueue,
)

# Filter in order of priority of execution
filter_list = [
    # AccountAge,
    # OpenPM,
    # Content,
    # URL,
    # CurseWords,
    SlowModeQueue,
]


__all__ = ("filter_list",)

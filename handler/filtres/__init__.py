from .filtres import (
    SlowModeQueueFilter,
    ContentFilter,
    OpenPMFilter,
    AccountAgeFilter,
    URLFilter,
    CurseWordsFilter,
)

# Filter in order of priority of execution
filter_list = [
    AccountAgeFilter,
    OpenPMFilter,
    ContentFilter,
    URLFilter,
    CurseWordsFilter,
    SlowModeQueueFilter,
]


__all__ = ("filter_list",)

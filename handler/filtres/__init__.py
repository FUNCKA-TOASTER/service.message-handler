from .filtres import (
    SlowModeQueueFilter,
    ContentFilter,
    OpenPMFilter,
    AccountAgeFilter
)

# Filter in order of priority of execution
filter_list = [
    AccountAgeFilter,
    OpenPMFilter,
    ContentFilter,
    SlowModeQueueFilter,
]



__all__ = (
    "filter_list",
)

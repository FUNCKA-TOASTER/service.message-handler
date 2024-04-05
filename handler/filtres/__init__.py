from .filtres import (
    SlowModeQueueFilter,
    ContentFilter,
    OpenPMFilter,
)

# Filter in order of priority of execution
filter_list = [
    OpenPMFilter,
    ContentFilter,
    SlowModeQueueFilter,
]



__all__ = (
    "filter_list",
)

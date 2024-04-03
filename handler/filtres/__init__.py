from .filtres import (
    SlowModeQueueFilter,
    ContentFilter,
)

# Filter in order of priority of execution
filter_list = [
    ContentFilter,
    SlowModeQueueFilter,
]



__all__ = (
    "filter_list",
)

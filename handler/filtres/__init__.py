from .filtres import (
    SlowModeQueueFilter,
)

# Filter in order of priority of execution
filter_list = [
    SlowModeQueueFilter,
]



__all__ = (
    "filter_list",
)

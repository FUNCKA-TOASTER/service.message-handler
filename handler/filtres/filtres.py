from .base import BaseFilter



# ------------------------------------------------------------------------
class Filter(BaseFilter):
    """Filter
    """
    NAME = "Filter"

    async def _handle(self, event: dict, kwargs) -> bool:
        return False

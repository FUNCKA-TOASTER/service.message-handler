from abc import ABC, abstractmethod


class ABCHandler(ABC):
    """The basic unit of event processing.
    Responsible for specific conditions and events
    events that occurred in the conversation and those that remained in VK event.

    Args:
        event (BaseEvent): Modified VKBotLongpoll event.
        api (VkApi): VK API object.

    Returns:
        bool: Handling status.
            True - handler triggered
            False - handler skiped
    """

    @abstractmethod
    async def _handle(self, event: dict, kwargs) -> bool:
        """Handling a custom event that returns the result of processing.
        It is used within the framework of one specific action with a custom event.

        Args:
            event (BaseEvent): Modified VKBotLongpoll event.
            api (VkApi): VK API object.

        Returns:
            bool: Handling status. Returns True if was handled.
        """

    async def __call__(self, event: dict, **kwargs) -> bool:
        """Calls the class as a function,
        handling the received input
        BaseEvent object.
        """
        return await self._handle(event, kwargs)

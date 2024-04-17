"""Module "producer"."""

from .body import Producer


class CustomProducer(Producer):
    """Custom producer class.
    Preferences for implimentation of custom
    functions for working with data that needs
    to be pushed into a queue inside RabbitMQ.
    """

    event_queues = {
        "warn": "warns",
    }

    async def initiate_warn(self, event, message, target, setting=None):
        queue = self.event_queues["warn"]
        data = {
            "warn_author": event.get("user_id"),
            "setting": setting,
            "text": message,
            "warn_target": target,
            "conversation": event.get("peer_id"),
        }
        await self._send_data(data, queue)


producer = CustomProducer()

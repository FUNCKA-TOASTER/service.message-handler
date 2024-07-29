"""Module "broker".

File:
    subscriber.py

About:
    File describing the implementation of the
    Subscriber class, which listens to Redis channels
    and deserializes incoming messages.
"""

from typing import Any, ByteString
import dill as pickle
from redis import Redis
from loguru import logger


class Subscriber:
    """Initializes the Subscriber with a Redis pubsub client.

    Descriprion:
        Class for subscribing to Redis channels and deserializing
        incoming messages.
    """

    def __init__(self, client: Redis) -> None:
        self.client = client.pubsub()

    def listen(self, channel_name: str) -> Any:
        """Listens to messages on a specified Redis channel and deserializes them.

        Args:
            channel_name (str): Name of the Redis channel to listen to.

        Yields:
            object: Deserialized object received from the channel.
        """

        self.client.subscribe(channel_name)
        logger.info("Waiting for events...")
        for event in self.client.listen():
            if event.get("type") == "message":
                deserialized = self.__deserialize(event.get("data"))
                logger.info(f"Recived new event: \n{deserialized}")
                yield deserialized

    @staticmethod
    def __deserialize(data: ByteString) -> Any:
        return pickle.loads(str=data)

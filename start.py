"""Service "service.message-handler".

File:
    start.py

About:
    This service is responsible for receiving custom
    events from the Redis channel "message", processing
    these events, and executing actions of filtering and
    content validation systems.
"""

import sys
from loguru import logger
from toaster.broker import Subscriber, build_connection
from data import TOASTER_DB
from handler import CommandHandler
import config


def setup_logger() -> None:
    logger.remove()
    logger.add(
        sys.stdout,
        colorize=True,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <red>{module}</red> | <level>{level}</level> | {message}",
        level="DEBUG",
    )


def setup_db() -> None:
    TOASTER_DB.create_tables()


async def main():
    """Program entry point."""

    setup_logger()
    setup_db()
    subscriber = Subscriber(client=build_connection(config.REDIS_CREDS))
    handler = CommandHandler()

    for event in subscriber.listen(channel_name=config.CHANNEL_NAME):
        handler(event)


if __name__ == "__main__":
    main()

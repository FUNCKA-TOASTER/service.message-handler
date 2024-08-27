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
from toaster import broker
from handler import MessageHandler
import config


def setup_logger() -> None:
    logger.remove()
    logger.add(
        sys.stdout,
        colorize=True,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <red>{module}</red> | <level>{level}</level> | {message}",
        level="DEBUG",
    )


def main():
    """Program entry point."""

    setup_logger()
    handler = MessageHandler()

    for event in broker.listen(queue_name=config.BROKER_QUEUE_NAME):
        handler(event)


if __name__ == "__main__":
    main()

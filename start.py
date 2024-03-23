"""Service "toaster.comman-handling-service".
About:
    ...
    
Author:
    Oidaho (Ruslan Bashinskii)
    oidahomain@gmail.com
"""
import asyncio
from consumer import consumer
from handler import message_handler
from logger import logger


async def main():
    """Entry point.
    """
    log_text = "Awaiting button events..."
    await logger.info(log_text)

    for data in consumer.listen_queue("messages"):
        log_text = f"Recived new event: {data}"
        await logger.info(log_text)

        await message_handler(data)



if __name__ == "__main__":
    asyncio.run(main())

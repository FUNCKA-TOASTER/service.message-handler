"""Module "broker".

File:
    connection.py

About:
    File describing Redis connection builder function.
"""

from redis import Redis
from toaster.credentials import RedisCredentials


def build_connection(creds: RedisCredentials) -> Redis:
    """Builds and returns a Redis connection object.

    Args:
        creds (RedisCredentials): The credentials required to connect to the Redis.

    Returns:
        Redis: A Redis connection object.
    """

    return Redis(
        host=creds.host,
        port=creds.port,
        db=creds.db,
    )

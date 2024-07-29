"""Module "credentials".

File:
    credentials.py

About:
    File describing data structures for storing
    credentials and setup configurations for any
    connections.
"""

from typing import NamedTuple


class AlchemyCredentials(NamedTuple):
    """Represents the credentials required to connect to a SQLAlchemy DBMS.

    Attributes:
        host (str): The hostname of the DBMS server.
        port (int): The port number on which the DBMS server is listening.
        user (str): The username for authentication.
        pswd (str): The password for authentication.
    """

    host: str
    port: int
    user: str
    pswd: str


class AlchemySetup(NamedTuple):
    """Represents the setup configuration for a SQLAlchemy database.

    Attributes:
        dialect (str): The database dialect (e.g., 'mysql', 'postgresql').
        driver (str): The database driver (e.g., 'pymysql', 'psycopg2').
        database (str): The name of the database to connect to.
    """

    dialect: str
    driver: str
    database: str


class RedisCredentials(NamedTuple):
    """Represents the credentials required to connect to a Redis server.

    Attributes:
        host (str): The hostname of the Redis server.
        port (int): The port number on which the Redis server is listening.
        db (int): The database number.
    """

    host: str
    port: int
    db: int

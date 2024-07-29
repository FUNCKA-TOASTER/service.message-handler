"""Module "database".

File:
    database.py

About:
    File describing the Databse class.
"""

from functools import singledispatch
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session, sessionmaker, declarative_base, DeclarativeBase
from loguru import logger


BaseModel = declarative_base()


class Database:
    """SQLA Database class."""

    def __init__(self, connection_uri: str, debug: bool = False) -> None:
        self._engine = create_engine(connection_uri, echo=debug, pool_pre_ping=True)
        self._session = sessionmaker(bind=self._engine, autoflush=False)

    @singledispatch
    def create_tables(self) -> None:
        """Creates all tables defined in the SQLAlchemy BaseModel."""

        logger.info("Creating tables...")
        BaseModel.metadata.create_all(self._engine)

    @singledispatch
    def drop_tables(self) -> None:
        """Drops all tables defined in the SQLAlchemy BaseModel."""

        logger.info("Droping tables...")
        BaseModel.metadata.create_all(self._engine)

    @create_tables.register
    def _(self, base: DeclarativeBase):
        """Creates all tables defined in the provided SQLAlchemy base model.

        Args:
            base (Any): The base model containing metadata for tables to be created.
        """
        base.metadata.create_all(self._engine)

    @drop_tables.register
    def _(self, base: DeclarativeBase):
        """Drops all tables defined in the provided SQLAlchemy base model.

        Args:
            base (Any): The base model containing metadata for tables to be dropped.
        """
        base.metadata.drop_all(self._engine)

    @property
    def engine(self) -> Engine:
        """Returns the SQLAlchemy engine instance.

        Returns:
            Engine: The SQLAlchemy engine instance.
        """
        return self._engine

    def make_session(self) -> Session:
        """Creates and returns a new SQLAlchemy session.

        Returns:
            Session: A new SQLAlchemy session.
        """
        return self._session()

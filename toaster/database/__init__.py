"""Module "database".

File:
    __init__.py

About:
    Initializing the "database" module.
"""

from .connection import build_connection_uri
from .database import Database, BaseModel
from .scripts import script


__all__ = (
    "build_connection_uri",  # A function to build SQLAlchemy connection URI.
    "script",  # A decorator to mark functions as custom scripts for SQLAlchemy.
    "Database",  # Class encapsulating SQLAlchemy database management operations.
    "BaseModel",  # Base class for SQLAlchemy models.
)

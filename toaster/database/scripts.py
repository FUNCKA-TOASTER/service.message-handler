"""Module "database".

File:
    scripts.py

About:
    File describing the SQLA script decorator.
"""

from typing import Callable, Optional, Any
from loguru import logger
from .database import Database


def script(auto_commit: bool = True, debug: bool = False) -> Callable:
    """A decorator that implements a custom script wrapper.

    The decorator allows you to mark a function
    as a custom script for sqlalchemy. Using
    this mechanism, you can conveniently call
    the desired set of actions in the right place.

    Example: ::

        @script(auto_commit=False)
        def add_user(session: Session, name: str, age: int):
            new_user = User(name=name, age=age)
            session.add(new_user)
            session.commit()

        @script(auto_commit=False)
        def ge_user(session: Session, id: int):
            user = session.get(User, {"id": id})
            return user

        # But calling requires Database instance
        add_user(db, name="Vasya", age=15)
        get_user(db, id=25611)
    """

    def decorator(func: Callable) -> Callable:
        def wrapper(db_instance: Database, *args, **kwargs) -> Optional[Any]:
            session = db_instance.make_session()
            try:
                result = func(session, *args, **kwargs)

                if auto_commit:
                    session.commit()

                return result

            except Exception as error:
                session.rollback()

                if debug:
                    _handle_exception(error, func)

            finally:
                session.close()

        return wrapper

    return decorator


def _handle_exception(error: Exception, func: Callable) -> None:
    text = (
        f"Script <{func.__name__}> execution failed. "
        "Transaction rolled back. \n"
        f"ErrorMessage: {error}"
    )
    logger.error(text)

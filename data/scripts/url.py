"""Module "scripts".

File:
    url.py

About:
    File describing custom SQLA scripts associated
    with the urls.
"""

from typing import Set
from sqlalchemy.orm import Session
from toaster.database import script
from data import Url, UrlStatus, UrlType


@script(auto_commit=False, debug=True)
def insert_pattern(
    session: Session, bpid: int, type: UrlType, status: UrlStatus, pattern: str
) -> None:
    new_pattern = Url(bpid=bpid, type=type, status=status, pattern=pattern)
    session.add(new_pattern)
    session.commit()


@script(auto_commit=False, debug=True)
def get_patterns(
    session: Session, bpid: int, type: UrlType, status: UrlStatus
) -> Set[str]:
    rows = (
        session.query(Url)
        .filter(
            Url.bpid == bpid,
            Url.type == type,
            Url.status == status,
        )
        .all()
    )
    return {row.pattern for row in rows}

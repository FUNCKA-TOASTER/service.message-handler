"""Module "scripts".

File:
    cursed.py

About:
    File describing custom SQLA scripts associated
    with the cursed words.
"""

from typing import List
from sqlalchemy.orm import Session
from toaster.database import script
from data import Cursed


@script(auto_commit=False, debug=True)
def insert_cursed(session: Session, bpid: int, word: str) -> None:
    new_pattern = Cursed(bpid=bpid, word=word)
    session.add(new_pattern)
    session.commit()


@script(auto_commit=False, debug=True)
def get_curse_words(session: Session, bpid: int) -> List[str]:
    rows = session.query(Cursed).filter(Cursed.bpid == bpid).all()
    return [row.word for row in rows]

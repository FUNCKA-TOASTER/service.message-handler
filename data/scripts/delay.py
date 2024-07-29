"""Module "scripts".

File:
    delay.py

About:
    File describing custom SQLA scripts associated
    with the delay.
"""

from typing import Optional
from sqlalchemy.orm import Session
from toaster.database import script
from data import Delay


@script(auto_commit=False, debug=True)
def get_setting_delay(session: Session, name: str, bpid: int) -> Optional[int]:
    setting = session.get(Delay, {"bpid": bpid, "setting": name})
    return setting.delay if setting else None


@script(auto_commit=False, debug=True)
def update_setting_delay(session: Session, name: str, bpid: int, delay: int) -> None:
    setting = session.get(Delay, {"bpid": bpid, "setting": name})
    setting.delay = delay
    session.commit()

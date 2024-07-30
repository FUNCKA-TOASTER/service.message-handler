"""Module "scripts".

File:
    user.py

About:
    File describing custom SQLA scripts associated
    with the user.
"""

from typing import Tuple, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from toaster.database import script
from data import (
    Permission,
    Staff,
    StaffRole,
    UserPermission,
    Warn,
    Queue,
    Delay,
)


WarnInfo = Tuple[int, datetime]


@script(auto_commit=False, debug=True)
def get_user_permission(
    session: Session, uuid: int, bpid: int, ignore_staff: bool = False
) -> UserPermission:
    if not ignore_staff:
        staff = session.get(Staff, {"uuid": uuid})
        if (staff is not None) and (StaffRole.TECH == staff.role):
            return UserPermission.administrator

    user = session.get(Permission, {"uuid": uuid, "bpid": bpid})
    return user.permission if user else UserPermission.user


@script(auto_commit=False, debug=True)
def set_user_permission(
    session: Session, lvl: UserPermission, uuid: int, bpid: int
) -> None:
    new_user = Permission(
        bpid=bpid,
        uuid=uuid,
        permission=lvl,
    )
    session.add(new_user)
    session.commit()


@script(auto_commit=False, debug=True)
def update_user_permission(
    session: Session, lvl: UserPermission, uuid: int, bpid: int
) -> None:
    user = session.get(Permission, {"uuid": uuid, "bpid": bpid})
    user.permission = lvl
    session.commit()


@script(auto_commit=False, debug=True)
def drop_user_permission(session: Session, uuid: int, bpid: int) -> None:
    user = session.get(Permission, {"uuid": uuid, "bpid": bpid})
    session.delete(user)
    session.commit()


@script(auto_commit=False, debug=True)
def get_user_warns(session: Session, uuid: int, bpid: int) -> Optional[WarnInfo]:
    warn = session.get(Warn, {"bpid": bpid, "uuid": uuid})
    return (warn.points, warn.expired) if warn else None


@script(auto_commit=False, debug=True)
def get_user_queue_status(session: Session, uuid: int, bpid: int) -> Optional[datetime]:
    queue = session.get(Queue, {"bpid": bpid, "uuid": uuid})
    return queue.expired if queue else None


@script(auto_commit=False, debug=True)
def insert_user_to_queue(session: Session, uuid: int, bpid: int, setting: str) -> None:
    setting = session.get(Delay, {"bpid": bpid, "setting": setting})
    new_queue_row = Queue(
        bpid=bpid,
        uuid=uuid,
        expired=(datetime.now() + timedelta(minutes=setting.delay)),
    )
    session.add(new_queue_row)
    session.commit()

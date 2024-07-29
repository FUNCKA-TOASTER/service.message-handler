"""Module "data".

File:
    annotations.py

About:
    File describing type annotations for SQLA table models.
"""

from typing import Annotated
from sqlalchemy.orm import mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.mysql import BIGINT

# This annotation defines the BPID (bot peer id) column with a BIGINT type.
# The column is a foreign key referencing the 'id' column in the 'peers' table.
# The 'ondelete' and 'onupdate' constraints ensure that changes to the 'peers' table are cascaded to this column.
BPID = Annotated[
    int,
    mapped_column(
        BIGINT,
        ForeignKey("peers.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
    ),
]

# This annotation defines the UUID (unique user id) column with a BIGINT type.
# The column is used as a primary key.
UUID = Annotated[int, mapped_column(BIGINT, primary_key=True)]

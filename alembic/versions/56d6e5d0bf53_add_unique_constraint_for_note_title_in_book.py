"""add unique constraint for note title in book

Revision ID: 56d6e5d0bf53
Revises: 0e91df108d7c
Create Date: 2026-03-20 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "56d6e5d0bf53"
down_revision: Union[str, Sequence[str], None] = "0e91df108d7c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(
        "uq_note_note_book_id_title",
        "note_note",
        ["book_id", "title"],
    )


def downgrade() -> None:
    op.drop_constraint("uq_note_note_book_id_title", "note_note", type_="unique")

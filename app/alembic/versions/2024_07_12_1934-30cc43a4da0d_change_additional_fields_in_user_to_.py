"""change additional fields in user to requirements

Revision ID: 30cc43a4da0d
Revises: a73d7223ab63
Create Date: 2024-07-12 19:34:53.232322

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "30cc43a4da0d"
down_revision: Union[str, None] = "a73d7223ab63"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "user", "first_name", existing_type=sa.VARCHAR(), nullable=False
    )
    op.alter_column(
        "user", "last_name", existing_type=sa.VARCHAR(), nullable=False
    )
    op.alter_column(
        "user",
        "birthday",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.Date(),
        nullable=False,
    )


def downgrade() -> None:
    op.alter_column(
        "user",
        "birthday",
        existing_type=sa.Date(),
        type_=postgresql.TIMESTAMP(),
        nullable=True,
    )
    op.alter_column(
        "user", "last_name", existing_type=sa.VARCHAR(), nullable=True
    )
    op.alter_column(
        "user", "first_name", existing_type=sa.VARCHAR(), nullable=True
    )

"""Create Donate table

Revision ID: a73d7223ab63
Revises: ca37abb8923f
Create Date: 2024-07-10 18:23:17.346929

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "a73d7223ab63"
down_revision: Union[str, None] = "ca37abb8923f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "donations",
        sa.Column("comment", sa.String(), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("full_amount", sa.Integer(), nullable=False),
        sa.Column("created_date", sa.DateTime(), nullable=False),
        sa.Column("invested_amount", sa.Integer(), nullable=False),
        sa.Column("fully_invested", sa.Boolean(), nullable=False),
        sa.Column("close_date", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("donations")
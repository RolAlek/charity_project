"""Create Project table

Revision ID: 4a75ea3edc6d
Revises: 
Create Date: 2024-07-05 20:32:36.426767

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '4a75ea3edc6d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'projects',
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('full_amount', sa.Integer(), nullable=False),
        sa.Column('invested_amount', sa.Integer(), nullable=False),
        sa.Column('fully_invested', sa.Boolean(), nullable=False),
        sa.Column('created_date', sa.DateTime(), nullable=False),
        sa.Column('close_date', sa.DateTime(), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
    )


def downgrade() -> None:
    op.drop_table('projects')

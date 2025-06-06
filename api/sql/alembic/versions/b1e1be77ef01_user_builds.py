"""create user_builds table

Revision ID: b1e1be77ef01
Revises: f4ca2cc40eeb
Create Date: 2025-06-01 00:00:00
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = 'b1e1be77ef01'
down_revision: Union[str, None] = 'f4ca2cc40eeb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'user_builds',
        sa.Column('build_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.String(255), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('build_name', sa.String(255), nullable=False),
        sa.Column('build_data', sa.JSON, nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table('user_builds')

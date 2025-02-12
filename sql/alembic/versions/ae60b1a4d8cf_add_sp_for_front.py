"""add sp for front

Revision ID: ae60b1a4d8cf
Revises: 650beec97ba7
Create Date: 2025-02-12 19:57:11.626481

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'ae60b1a4d8cf'
down_revision: Union[str, None] = '650beec97ba7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("DROP PROCEDURE IF EXISTS GetModifiersByType;")

    op.execute("""
        CREATE PROCEDURE GetModifiersByType(IN mod_type VARCHAR(255))
        BEGIN
            SELECT * FROM modifiers WHERE modifier_type LIKE CONCAT('%', mod_type, '%');
        END;
        """)


def downgrade() -> None:
    op.execute("DROP PROCEDURE IF EXISTS GetModifiersByType;")

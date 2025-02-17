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
    op.alter_column('modifiers', 'modifier_name', existing_type=sa.String(255), type_=sa.JSON())

    op.execute("DROP PROCEDURE IF EXISTS AddModifier;")
    op.execute("DROP PROCEDURE IF EXISTS UpdateModifier;")
    op.execute("DROP PROCEDURE IF EXISTS GetModifiersByType;")

    op.execute("""
        CREATE PROCEDURE GetModifiersByType(IN mod_type VARCHAR(255))
        BEGIN
            SELECT * FROM modifiers WHERE modifier_type LIKE CONCAT('%', mod_type, '%');
        END;
        """)

    op.execute("""
            CREATE PROCEDURE UpdateModifier(
                IN p_modifier_id INTEGER,
                IN p_modifier_name JSON,
                IN p_modifier_type VARCHAR(150),
                IN p_modifier_statistiques VARCHAR(1024),
                IN p_modifier_stack_id VARCHAR(50),
                IN p_modifier_stack_description TEXT,
                IN p_modifier_displaydata JSON
            )
            BEGIN
                UPDATE modifiers
                SET 
                    modifier_name = p_modifier_name,
                    modifier_type = p_modifier_type,
                    modifier_statistiques = p_modifier_statistiques,
                    modifier_stack_id = p_modifier_stack_id,
                    modifier_stack_description = p_modifier_stack_description,
                    modifier_displaydata = p_modifier_displaydata
                WHERE p_modifier_id = modifier_id;
            END;
            """)

    op.execute("""
            CREATE PROCEDURE AddModifier(
                IN p_modifier_id INTEGER,
                IN p_modifier_name JSON,
                IN p_modifier_type VARCHAR(150),
                IN p_modifier_statistiques VARCHAR(1024),
                IN p_modifier_stack_id VARCHAR(50),
                IN p_modifier_stack_description TEXT,
                IN p_modifier_displaydata JSON
            )
            BEGIN
                INSERT INTO modifiers (modifier_id, modifier_name, modifier_type, modifier_statistiques, modifier_stack_id, modifier_stack_description, modifier_displaydata)
                VALUES (p_modifier_id, p_modifier_name, p_modifier_type, p_modifier_statistiques, p_modifier_stack_id, p_modifier_stack_description, p_modifier_displaydata);
            END;
            """)


def downgrade() -> None:
    op.execute("DROP PROCEDURE IF EXISTS AddModifier;")
    op.execute("DROP PROCEDURE IF EXISTS UpdateModifier;")
    op.execute("DROP PROCEDURE IF EXISTS GetModifiersByType;")
    op.alter_column('modifiers', 'modifier_name', existing_type=sa.JSON(), type_=sa.String(255))

"""update item table + sp

Revision ID: 650beec97ba7
Revises: 0cdbe6a341e6
Create Date: 2025-02-05 17:20:31.457675

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '650beec97ba7'
down_revision: Union[str, None] = '0cdbe6a341e6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Vérifier si 'modifier_displaydata' existe déjà
    op.add_column('modifiers', sa.Column('modifier_displaydata', sa.JSON(), nullable=True))

    # Modification de item_statistiques de TEXT à JSON
    with op.batch_alter_table('items') as batch_op:
        batch_op.alter_column('item_statistiques', type_=sa.JSON(), existing_type=sa.Text())
        batch_op.alter_column("item_Goals", existing_type=sa.String(50), nullable=True)

    op.execute("DROP PROCEDURE IF EXISTS AddItem;")
    op.execute("DROP PROCEDURE IF EXISTS UpdateItem;")
    op.execute("DROP PROCEDURE IF EXISTS AddModifier;")
    op.execute("DROP PROCEDURE IF EXISTS UpdateModifier;")

    op.execute("""
        CREATE PROCEDURE AddItem(
            IN p_item_id INT,
            IN p_item_name JSON,
            IN p_item_type VARCHAR(50),
            IN p_item_goals VARCHAR(50),
            IN p_item_capabilities TEXT,
            IN p_item_statistiques JSON,
            IN p_item_displaydata JSON
        )
        BEGIN
            INSERT INTO items (item_id, item_name, item_type, item_goals, item_capabilities, item_statistiques, item_displaydata)
            VALUES (p_item_id, p_item_name, p_item_type, p_item_goals, p_item_capabilities, p_item_statistiques, p_item_displaydata);
        END;
        """)

    op.execute("""
        CREATE PROCEDURE UpdateItem(
            IN p_item_id INT,
            IN p_item_name JSON,
            IN p_item_type VARCHAR(50),
            IN p_item_goals VARCHAR(50),
            IN p_item_capabilities TEXT,
            IN p_item_statistiques JSON,
            in p_item_displaydata JSON
        )
        BEGIN
            UPDATE items
            SET item_name = p_item_name, 
                item_type = p_item_type, 
                item_goals = p_item_goals, 
                item_capabilities = p_item_capabilities,
                item_statistiques = p_item_statistiques,
                item_displaydata = p_item_displaydata
            WHERE item_id = p_item_id;
        END;
        """)

    op.execute("""
        CREATE PROCEDURE AddModifier(
            IN p_modifier_id INTEGER,
            IN p_modifier_name VARCHAR(255),
            IN p_modifier_type VARCHAR(150),
            IN p_modifier_statistiques VARCHAR(1024),
            IN p_modifier_stack_id VARCHAR(50),
            IN p_modifier_stack_description TEXT,
            in p_modifier_displaydata JSON
        )
        BEGIN
            INSERT INTO modifiers (modifier_id, modifier_name, modifier_type, modifier_statistiques, modifier_stack_id, modifier_stack_description, modifier_displaydata)
            VALUES (p_modifier_id, p_modifier_name, p_modifier_type, p_modifier_statistiques, p_modifier_stack_id, p_modifier_stack_description, p_modifier_displaydata);
        END;
        """)

    op.execute("""
        CREATE PROCEDURE UpdateModifier(
            IN p_modifier_id INTEGER,
            IN p_modifier_name VARCHAR(255),
            IN p_modifier_type VARCHAR(150),
            IN p_modifier_statistiques VARCHAR(1024),
            IN p_modifier_stack_id VARCHAR(50),
            IN p_modifier_stack_description TEXT,
            in p_modifier_displaydata JSON
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
    pass


def downgrade() -> None:
    # Suppression de la colonne displaydata
    conn = op.get_bind()
    result = conn.execute(text("SHOW COLUMNS FROM items LIKE 'displaydata'"))
    column_exists = result.fetchone()

    if column_exists:
        op.drop_column('items', 'displaydata')

    # Revert item_statistiques en TEXT
    with op.batch_alter_table('items') as batch_op:
        batch_op.alter_column('item_statistiques', type_=sa.Text(), existing_type=sa.JSON())
        batch_op.alter_column("item_Goals", existing_type=sa.String(50), nullable=False)

    # Supprimer la procédure stockée
    op.execute("DROP PROCEDURE IF EXISTS AddItem;")
    op.execute("DROP PROCEDURE IF EXISTS UpdateItem;")
    pass
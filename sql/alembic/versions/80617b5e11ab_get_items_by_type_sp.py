"""get_Items_by_type SP

Revision ID: 80617b5e11ab
Revises: 35db623c458d
Create Date: 2025-02-23 19:51:03.416520

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '80617b5e11ab'
down_revision: Union[str, None] = '35db623c458d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("DROP PROCEDURE IF EXISTS GetItemsByType;")

    op.execute("DROP PROCEDURE IF EXISTS AddItem;")
    op.execute("DROP PROCEDURE IF EXISTS UpdateItem;")

    op.execute("""
        CREATE PROCEDURE GetItemsByType(IN item VARCHAR(255))
        BEGIN
            SELECT * FROM items WHERE item_type LIKE CONCAT('%', item, '%');
        END;
        """)

    op.execute("""
            CREATE PROCEDURE AddItem(
                IN p_item_id INT,
                IN p_item_name JSON,
                IN p_item_type VARCHAR(50),
                IN p_item_goals VARCHAR(50),
                IN p_item_capabilities JSON,
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
                IN p_item_capabilities JSON,
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

    # On modifie la colonne item_name pour qu'elle soit de type JSON
    op.alter_column(
        'items',
        'item_name',
        type_=sa.JSON(),
        existing_type=sa.String(length=255),
        nullable=True  # Adaptez selon votre schéma
    )

    # On modifie la colonne item_capabilities pour qu'elle soit de type JSON
    op.alter_column(
        'items',
        'item_capabilities',
        type_=sa.JSON(),
        existing_type=sa.Text(),
        nullable=True  # Adaptez selon votre schéma
    )

def downgrade() -> None:
    op.execute("DROP PROCEDURE IF EXISTS GetItemsByType;")
    op.execute("DROP PROCEDURE IF EXISTS AddItem;")
    op.execute("DROP PROCEDURE IF EXISTS UpdateItem;")
    # En cas de rollback, on revient aux types d'origine
    op.alter_column(
        'items',
        'item_capabilities',
        type_=sa.Text(),
        existing_type=sa.JSON(),
        nullable=True
    )

    op.alter_column(
        'items',
        'item_name',
        type_=sa.String(length=255),
        existing_type=sa.JSON(),
        nullable=True
    )

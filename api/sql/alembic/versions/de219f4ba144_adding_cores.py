"""adding cores

Revision ID: de219f4ba144
Revises: 7af09af6c73d
Create Date: 2025-04-12 21:32:42.473859

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'de219f4ba144'
down_revision: Union[str, None] = '7af09af6c73d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Table core_type : stocke l'identifiant et le nom du core
    op.create_table(
        'core_type',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('core_type_id', sa.Integer, nullable=False, unique=True),
        sa.Column('core_type', sa.Integer, sa.ForeignKey('translation_strings.id'), nullable=False)
    )

    # 2. Table core_option : chaque type de core peut avoir plusieurs options
    op.create_table(
        'core_option',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        # Référence le core_type auquel appartient cette option.
        sa.Column('core_type_id', sa.Integer, sa.ForeignKey('core_type.core_type_id'), nullable=False),
        sa.Column('core_option_id', sa.Integer, nullable=False)
    )

    # 3. Table core_option_detail : pour chaque option, stocke les détails (grade et item requis)
    op.create_table(
        'core_option_detail',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('core_option_id', sa.Integer, nullable=False),
        sa.Column('core_option_grade', sa.Integer, nullable=True),
        sa.Column('required_meta_type', sa.String(255), nullable=False),
        sa.Column('required_meta_id', sa.Integer, nullable=False),
        sa.Column('required_count', sa.Integer, nullable=False)
    )

    # 4. Table core_available_item_option : pour chaque option, stocke les options disponibles
    op.create_table(
        'core_available_item_option',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('core_type_id', sa.Integer, sa.ForeignKey('core_type.core_type_id'), nullable=False),
        sa.Column('core_option_id', sa.Integer, nullable=False),
        sa.Column('option_type', sa.String(255), nullable=False),
        sa.Column('option_grade', sa.Integer, nullable=False),
        sa.Column('stat_id', sa.Integer, nullable=False),
        sa.Column('operator_type', sa.String(255), nullable=False),
        sa.Column('min_stat_value', sa.Float, nullable=False),
        sa.Column('max_stat_value', sa.Float, nullable=False),
        sa.Column('rate', sa.Integer, nullable=False)
    )

    op.create_table(
        'core_slot',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('core_slot_id', sa.Integer, unique=True, nullable=False),
        sa.Column('available_weapon', sa.Integer, sa.ForeignKey('weapon.weapon_id'), nullable=False),
        sa.Column('available_core_type', sa.Integer, sa.ForeignKey('core_type.core_type_id'), nullable=False)
    )

    op.execute("DROP PROCEDURE IF EXISTS GetCoreSlot;")
    op.execute(
        """
        CREATE PROCEDURE GetCoreSlot(
            IN p_core_slot_id INT
        )
        BEGIN
            SELECT * FROM core_slot WHERE core_slot_id = p_core_slot_id;
        END
        """
    )

    op.execute("DROP PROCEDURE IF EXISTS AddCoreSlot;")
    op.execute(
        """
        CREATE PROCEDURE AddCoreSlot(
            IN p_core_slot_id INT,
            IN p_available_weapon INT,
            IN p_available_core_type INT,
            OUT new_id INT
        )
        BEGIN
            INSERT INTO core_slot(core_slot_id, available_weapon, available_core_type)
            VALUES (p_core_slot_id, p_available_weapon, p_available_core_type);
            SET new_id = LAST_INSERT_ID();
        END
        """
    )

    op.execute("DROP PROCEDURE IF EXISTS UpdateCoreSlot;")
    op.execute(
        """
        CREATE PROCEDURE UpdateCoreSlot(
            IN p_id INT,
            IN p_core_slot_id INT,
            IN p_available_weapon INT,
            IN p_available_core_type INT
        )
        BEGIN
            UPDATE core_slot
            SET core_slot_id = p_core_slot_id,
                available_weapon = p_available_weapon,
                available_core_type = p_available_core_type
            WHERE id = p_id;
        END
        """
    )

    op.execute("DROP PROCEDURE IF EXISTS GetCoreType;")
    op.execute(
        """
        CREATE PROCEDURE GetCoreType(
            IN p_core_type_id INT
        )
        BEGIN
            SELECT * FROM core_type WHERE core_type_id = p_core_type_id;
        END
        """
    )

    # Procédure pour ajouter un core_type et retourner l'id inséré.
    op.execute("DROP PROCEDURE IF EXISTS AddCoreType;")
    op.execute(
        """
        CREATE PROCEDURE AddCoreType(
            IN p_core_type_id VARCHAR(255),
            IN p_core_type VARCHAR(255),
            OUT new_id INT
        )
        BEGIN
            INSERT INTO core_type(core_type_id, core_type)
            VALUES (p_core_type_id, p_core_type);
            SET new_id = LAST_INSERT_ID();
        END
        """
    )

    # Procédure pour mettre à jour un core_type existant.
    op.execute("DROP PROCEDURE IF EXISTS UpdateCoreType;")
    op.execute(
        """
        CREATE PROCEDURE UpdateCoreType(
            IN p_id INT,
            IN p_core_type_id VARCHAR(255),
            IN p_core_type VARCHAR(255)
        )
        BEGIN
            UPDATE core_type
            SET core_type_id = p_core_type_id,
                core_type = p_core_type
            WHERE id = p_id;
        END
        """
    )

    op.execute("DROP PROCEDURE IF EXISTS GetCoreOption;")
    op.execute(
        """
        CREATE PROCEDURE GetCoreOption(
            IN p_core_type_id INT,
            IN p_core_option_id INT
        )
        BEGIN
            SELECT * FROM core_option 
            WHERE core_type_id = p_core_type_id 
              AND core_option_id = p_core_option_id;
        END
        """
    )

    op.execute("DROP PROCEDURE IF EXISTS AddCoreOption;")
    op.execute(
        """
        CREATE PROCEDURE AddCoreOption(
            IN p_core_type_id INT,
            IN p_core_option_id INT,
            OUT new_id INT
        )
        BEGIN
            INSERT INTO core_option(core_type_id, core_option_id)
            VALUES (p_core_type_id, p_core_option_id);
            SET new_id = LAST_INSERT_ID();
        END
        """
    )

    op.execute("DROP PROCEDURE IF EXISTS UpdateCoreOption;")
    op.execute(
        """
        CREATE PROCEDURE UpdateCoreOption(
            IN p_id INT,
            IN p_core_type_id INT,
            IN p_core_option_id INT
        )
        BEGIN
            UPDATE core_option
            SET core_type_id = p_core_type_id,
                core_option_id = p_core_option_id
            WHERE id = p_id;
        END
        """
    )

    op.execute("DROP PROCEDURE IF EXISTS GetCoreOptionDetail;")
    op.execute(
        """
        CREATE PROCEDURE GetCoreOptionDetail(
            IN p_required_meta_id INT
        )
        BEGIN
            SELECT * FROM core_option_detail 
            WHERE required_meta_id = p_required_meta_id;
        END
        """
    )

    op.execute("DROP PROCEDURE IF EXISTS AddCoreOptionDetail;")
    op.execute(
        """
        CREATE PROCEDURE AddCoreOptionDetail(
            IN p_core_option_id INT,
            IN p_core_option_grade INT,
            IN p_required_meta_type VARCHAR(255),
            IN p_required_meta_id INT,
            IN p_required_count INT,
            OUT new_id INT
        )
        BEGIN
            INSERT INTO core_option_detail(core_option_id, core_option_grade, required_meta_type, required_meta_id, required_count)
            VALUES (p_core_option_id, p_core_option_grade, p_required_meta_type, p_required_meta_id, p_required_count);
            SET new_id = LAST_INSERT_ID();
        END
        """
    )

    op.execute("DROP PROCEDURE IF EXISTS UpdateCoreOptionDetail;")
    op.execute(
        """
        CREATE PROCEDURE UpdateCoreOptionDetail(
            IN p_id INT,
            IN p_core_option_id INT,
            IN p_core_option_grade INT,
            IN p_required_meta_type VARCHAR(255),
            IN p_required_meta_id INT,
            IN p_required_count INT
        )
        BEGIN
            UPDATE core_option_detail
            SET core_option_id = p_core_option_id,
                core_option_grade = p_core_option_grade,
                required_meta_type = p_required_meta_type,
                required_meta_id = p_required_meta_id,
                required_count = p_required_count
            WHERE id = p_id;
        END
        """
    )

    op.execute("DROP PROCEDURE IF EXISTS GetCoreAvailableItemOption;")
    op.execute(
        """
        CREATE PROCEDURE GetCoreAvailableItemOption(
            IN p_core_option_id INT,
            IN p_option_grade INT,
            IN p_stat_id INT
        )
        BEGIN
            SELECT * FROM core_available_item_option
            WHERE core_option_id = p_core_option_id
                AND option_grade = p_option_grade
                AND stat_id = p_stat_id;
        END
        """
    )

    op.execute("DROP PROCEDURE IF EXISTS AddCoreAvailableItemOption;")
    op.execute(
        """
        CREATE PROCEDURE AddCoreAvailableItemOption(
            IN p_core_type_id INT,
            IN p_core_option_id INT,
            IN p_option_type VARCHAR(255),
            IN p_option_grade INT,
            IN p_stat_id INT,
            IN p_operator_type VARCHAR(255),
            IN p_min_stat_value FLOAT,
            IN p_max_stat_value FLOAT,
            IN p_rate INT,
            OUT new_id INT
        )
        BEGIN
            INSERT INTO core_available_item_option(core_type_id, core_option_id, option_type, option_grade, stat_id, operator_type, min_stat_value, max_stat_value, rate)
            VALUES (p_core_type_id, p_core_option_id, p_option_type, p_option_grade, p_stat_id, p_operator_type, p_min_stat_value, p_max_stat_value, p_rate);
            SET new_id = LAST_INSERT_ID();
        END
        """
    )

    op.execute("DROP PROCEDURE IF EXISTS UpdateCoreAvailableItemOption;")
    op.execute(
        """
        CREATE PROCEDURE UpdateCoreAvailableItemOption(
            IN p_id INT,
            IN p_core_type_id INT,
            IN p_core_option_id INT,
            IN p_option_type VARCHAR(255),
            IN p_option_grade INT,
            IN p_stat_id INT,
            IN p_operator_type VARCHAR(255),
            IN p_min_stat_value FLOAT,
            IN p_max_stat_value FLOAT,
            IN p_rate INT
        )
        BEGIN
            UPDATE core_available_item_option
            SET core_type_id = p_core_type_id,
                core_option_id = p_core_option_id,
                option_type = p_option_type,
                option_grade = p_option_grade,
                stat_id = p_stat_id,
                operator_type = p_operator_type,
                min_stat_value = p_min_stat_value,
                max_stat_value = p_max_stat_value,
                rate = p_rate
            WHERE id = p_id;
        END
        """
    )

    ## clean previous
    op.execute("DROP PROCEDURE IF EXISTS AddBuild;")
    op.execute("DROP PROCEDURE IF EXISTS AddBuildModifiers;")
    op.execute("DROP PROCEDURE IF EXISTS AddItem;")
    op.execute("DROP PROCEDURE IF EXISTS AddModifier;")
    op.execute("DROP PROCEDURE IF EXISTS DeleteBuild;")
    op.execute("DROP PROCEDURE IF EXISTS DeleteBuildModifiers;")
    op.execute("DROP PROCEDURE IF EXISTS DeleteItem;")
    op.execute("DROP PROCEDURE IF EXISTS DeleteModifier;")
    op.execute("DROP PROCEDURE IF EXISTS GetBuild;")
    op.execute("DROP PROCEDURE IF EXISTS GetBuildModifiers;")
    op.execute("DROP PROCEDURE IF EXISTS GetItem;")
    op.execute("DROP PROCEDURE IF EXISTS GetItemByType;")
    op.execute("DROP PROCEDURE IF EXISTS UpdateBuild;")
    op.execute("DROP PROCEDURE IF EXISTS UpdateItem;")
    op.execute("DROP PROCEDURE IF EXISTS UpdateModifier;")

    op.execute("DROP TABLE IF EXISTS build_modifiers;")
    op.execute("DROP TABLE IF EXISTS modifiers;")
    op.execute("DROP TABLE IF EXISTS builds;")
    op.execute("DROP TABLE IF EXISTS items;")

def downgrade() -> None:
    op.execute("DROP PROCEDURE IF EXISTS UpdateCoreAvailableItemOption;")
    op.execute("DROP PROCEDURE IF EXISTS AddCoreAvailableItemOption;")
    op.execute("DROP PROCEDURE IF EXISTS GetCoreAvailableItemOption;")
    op.execute("DROP PROCEDURE IF EXISTS UpdateCoreOptionDetail;")
    op.execute("DROP PROCEDURE IF EXISTS AddCoreOptionDetail;")
    op.execute("DROP PROCEDURE IF EXISTS GetCoreOptionDetail;")
    op.execute("DROP PROCEDURE IF EXISTS UpdateCoreOption;")
    op.execute("DROP PROCEDURE IF EXISTS UpdateCoreSlot;")
    op.execute("DROP PROCEDURE IF EXISTS UpdateCoreType;")
    op.execute("DROP PROCEDURE IF EXISTS AddCoreOption;")
    op.execute("DROP PROCEDURE IF EXISTS GetCoreOption;")
    op.execute("DROP PROCEDURE IF EXISTS AddCoreType;")
    op.execute("DROP PROCEDURE IF EXISTS GetCoreType;")
    op.execute("DROP PROCEDURE IF EXISTS AddCoreSlot;")
    op.execute("DROP PROCEDURE IF EXISTS GetCoreSlot;")

    op.drop_table('core_available_item_option')
    op.drop_table('core_option_detail')
    op.drop_table('core_option')
    op.drop_table('core_slot')
    op.drop_table('core_type')



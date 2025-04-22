"""adding modules

Revision ID: 922731919809
Revises: f4ca2cc40eeb
Create Date: 2025-04-21 12:53:20.028604

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '922731919809'
down_revision: Union[str, None] = 'f4ca2cc40eeb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ---------- Tables principales ----------------------------------------
    op.create_table(
        "module",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("module_name_id", sa.Integer, sa.ForeignKey("translation_strings.id"), nullable=False),
        sa.Column("module_id", sa.Integer, nullable=False, unique=True),
        sa.Column("image_url", sa.String(255)),
        sa.Column("module_type", sa.Integer, sa.ForeignKey("translation_strings.id")),
        sa.Column("module_tier_id", sa.String(255)),
        sa.Column("module_socket_type", sa.Integer, sa.ForeignKey("translation_strings.id")),
        sa.Column("module_class", sa.Integer, sa.ForeignKey("translation_strings.id")),
        sa.Column("available_weapon_type", sa.Text),
        sa.Column("available_descendant_id", sa.Text),
        sa.Column("available_module_slot_type", sa.Text),
    )

    op.create_table(
        "module_stat",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("module_id", sa.Integer, sa.ForeignKey("module.module_id"), nullable=False),
        sa.Column("level", sa.Integer, nullable=False),
        sa.Column("module_capacity", sa.Integer, nullable=False),
        sa.Column("value", sa.JSON, nullable=False),
    )

    # ---------- Procédures stockées ---------------------------------------
    op.execute("DROP PROCEDURE IF EXISTS GetModule;")
    op.execute(
        """
        CREATE PROCEDURE GetModule(IN p_module_id INT)
        BEGIN
            SELECT * FROM module WHERE module_id = p_module_id;
        END
        """
    )

    op.execute("DROP PROCEDURE IF EXISTS AddModule;")
    op.execute(
        """
        CREATE PROCEDURE AddModule(
            IN  p_module_name_id INT,
            IN  p_module_id INT,
            IN  p_image_url VARCHAR(255),
            IN  p_module_type INT,
            IN  p_module_tier_id VARCHAR(255),
            IN  p_module_socket_type INT,
            IN  p_module_class INT,
            IN  p_available_weapon_type TEXT,
            IN  p_available_descendant_id TEXT,
            IN  p_available_module_slot_type TEXT,
            OUT new_id INT
        )
        BEGIN
            INSERT INTO module(
                module_name_id, module_id, image_url, module_type, module_tier_id,
                module_socket_type, module_class,
                available_weapon_type, available_descendant_id, available_module_slot_type
            )
            VALUES (
                p_module_name_id, p_module_id, p_image_url, p_module_type, p_module_tier_id,
                p_module_socket_type, p_module_class,
                p_available_weapon_type, p_available_descendant_id, p_available_module_slot_type
            );
            SET new_id = LAST_INSERT_ID();
        END
        """
    )

    op.execute("DROP PROCEDURE IF EXISTS UpdateModule;")
    op.execute(
        """
        CREATE PROCEDURE UpdateModule(
            IN p_id INT,
            IN p_module_name_id INT,
            IN p_module_id INT,
            IN p_image_url VARCHAR(255),
            IN p_module_type INT,
            IN p_module_tier_id VARCHAR(255),
            IN p_module_socket_type INT,
            IN p_module_class INT,
            IN p_available_weapon_type TEXT,
            IN p_available_descendant_id TEXT,
            IN p_available_module_slot_type TEXT
        )
        BEGIN
            UPDATE module
            SET module_name_id            = p_module_name_id,
                module_id                = p_module_id,
                image_url                = p_image_url,
                module_type              = p_module_type,
                module_tier_id           = p_module_tier_id,
                module_socket_type       = p_module_socket_type,
                module_class             = p_module_class,
                available_weapon_type    = p_available_weapon_type,
                available_descendant_id  = p_available_descendant_id,
                available_module_slot_type = p_available_module_slot_type
            WHERE id = p_id;
        END
        """
    )

    op.execute("DROP PROCEDURE IF EXISTS GetModuleStat;")
    op.execute(
        """
        CREATE PROCEDURE GetModuleStat(IN p_module_id INT, IN p_level INT)
        BEGIN
            SELECT * FROM module_stat
            WHERE module_id = p_module_id AND level = p_level;
        END
        """
    )

    op.execute("DROP PROCEDURE IF EXISTS AddModuleStat;")
    op.execute(
        """
        CREATE PROCEDURE AddModuleStat(
            IN  p_module_id INT,
            IN  p_level INT,
            IN  p_module_capacity INT,
            IN  p_value JSON,
            OUT new_id INT
        )
        BEGIN
            INSERT INTO module_stat(module_id, level, module_capacity, value)
            VALUES (p_module_id, p_level, p_module_capacity, p_value);
            SET new_id = LAST_INSERT_ID();
        END
        """
    )

    op.execute("DROP PROCEDURE IF EXISTS UpdateModuleStat;")
    op.execute(
        """
        CREATE PROCEDURE UpdateModuleStat(
            IN p_id INT,
            IN p_module_id INT,
            IN p_level INT,
            IN p_module_capacity INT,
            IN p_value JSON
        )
        BEGIN
            UPDATE module_stat
            SET module_id       = p_module_id,
                level           = p_level,
                module_capacity = p_module_capacity,
                value           = p_value
            WHERE id = p_id;
        END
        """
    )


def downgrade() -> None:
    op.execute("DROP PROCEDURE IF EXISTS UpdateModuleStat;")
    op.execute("DROP PROCEDURE IF EXISTS AddModuleStat;")
    op.execute("DROP PROCEDURE IF EXISTS GetModuleStat;")
    op.execute("DROP PROCEDURE IF EXISTS UpdateModule;")
    op.execute("DROP PROCEDURE IF EXISTS AddModule;")
    op.execute("DROP PROCEDURE IF EXISTS GetModule;")

    op.drop_table("module_stat")
    op.drop_table("module")
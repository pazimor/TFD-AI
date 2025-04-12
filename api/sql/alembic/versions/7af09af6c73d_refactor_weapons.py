"""Refactor Weapons

Revision ID: 7af09af6c73d
Revises: 57b3648b9f93
Create Date: 2025-04-11 18:43:17.085594

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7af09af6c73d'
down_revision: Union[str, None] = '57b3648b9f93'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Création de la table principale "weapon" avec une référence vers "translation_strings"
    op.create_table(
        'weapon',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('weapon_name_id', sa.Integer, sa.ForeignKey('translation_strings.id'), nullable=False, unique=True),
        sa.Column('weapon_id', sa.Integer, nullable=False, unique=True),
        sa.Column('image_url', sa.String(255), nullable=True),
        sa.Column('weapon_type', sa.Integer, sa.ForeignKey('translation_strings.id'), nullable=True),
        sa.Column('weapon_tier_id', sa.String(255), nullable=True),
        sa.Column('weapon_rounds_type', sa.Integer, sa.ForeignKey('translation_strings.id'), nullable=True),
        sa.Column('available_core_slot', sa.Integer, nullable=True),
        sa.Column('weapon_perk_ability_name', sa.Integer, sa.ForeignKey('translation_strings.id'), nullable=True),
        sa.Column('weapon_perk_ability_description', sa.Integer, sa.ForeignKey('translation_strings.id'), nullable=True),
        sa.Column('weapon_perk_ability_image_url', sa.String(255), nullable=True),
        sa.Column('firearm_atk_type', sa.Integer, nullable=True),
        sa.Column('firearm_atk_value', sa.Integer, nullable=True)
    )

    op.create_table(
        'weapon_base_stat',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('weapon_id', sa.Integer, sa.ForeignKey('weapon.weapon_id'), nullable=False),
        sa.Column('stat_id', sa.Integer, sa.ForeignKey('translation_strings.id'), nullable=False), ## integer
        sa.Column('stat_value', sa.Integer, nullable=False)
    )

    op.execute("DROP PROCEDURE IF EXISTS GetWeapon;")
    op.execute(
        """
        CREATE PROCEDURE GetWeapon(
            IN p_weapon_id INT
        )
        BEGIN
            SELECT * FROM weapon
            WHERE weapon_id = p_weapon_id;
        END
        """
    )

    op.execute("DROP PROCEDURE IF EXISTS AddWeapon;")
    op.execute(
        """
        CREATE PROCEDURE AddWeapon(
            IN p_weapon_name_id INT,
            IN p_weapon_id INT,
            IN p_image_url VARCHAR(255),
            IN p_weapon_type INT,
            IN p_weapon_tier_id VARCHAR(255),
            IN p_weapon_rounds_type INT,
            IN p_available_core_slot INT,
            IN p_weapon_perk_ability_name INT,
            IN p_weapon_perk_ability_description INT,
            IN p_weapon_perk_ability_image_url VARCHAR(255),
            IN p_firearm_atk_type INT,
            IN p_firearm_atk_value INT,
            OUT new_id INT
        )
        BEGIN
            INSERT INTO weapon(
                weapon_name_id,
                weapon_id,
                image_url,
                weapon_type,
                weapon_tier_id,
                weapon_rounds_type,
                available_core_slot,
                weapon_perk_ability_name,
                weapon_perk_ability_description,
                weapon_perk_ability_image_url,
                firearm_atk_type,
                firearm_atk_value
            )
            VALUES (
                p_weapon_name_id,
                p_weapon_id,
                p_image_url,
                p_weapon_type,
                p_weapon_tier_id,
                p_weapon_rounds_type,
                p_available_core_slot,
                p_weapon_perk_ability_name,
                p_weapon_perk_ability_description,
                p_weapon_perk_ability_image_url,
                p_firearm_atk_type,
                p_firearm_atk_value
            );
            SET new_id = LAST_INSERT_ID();
        END
        """
    )

    op.execute("DROP PROCEDURE IF EXISTS UpdateWeapon;")
    op.execute(
        """
        CREATE PROCEDURE UpdateWeapon(
            IN p_id INT,
            IN p_weapon_name_id INT,
            IN p_weapon_id INT,
            IN p_image_url VARCHAR(255),
            IN p_weapon_type INT,
            IN p_weapon_tier_id VARCHAR(255),
            IN p_weapon_rounds_type INT,
            IN p_available_core_slot INT,
            IN p_weapon_perk_ability_name INT,
            IN p_weapon_perk_ability_description INT,
            IN p_weapon_perk_ability_image_url VARCHAR(255),
            IN p_firearm_atk_type INT,
            IN p_firearm_atk_value INT
        )
        BEGIN
            UPDATE weapon
            SET weapon_name_id = p_weapon_name_id,
                weapon_id = p_weapon_id,
                image_url = p_image_url,
                weapon_type = p_weapon_type,
                weapon_tier_id = p_weapon_tier_id,
                weapon_rounds_type = p_weapon_rounds_type,
                available_core_slot = p_available_core_slot,
                weapon_perk_ability_name = p_weapon_perk_ability_name,
                weapon_perk_ability_description = p_weapon_perk_ability_description,
                weapon_perk_ability_image_url = p_weapon_perk_ability_image_url,
                firearm_atk_type = p_firearm_atk_type,
                firearm_atk_value = p_firearm_atk_value
            WHERE id = p_id;
        END
        """
    )

    op.execute("DROP PROCEDURE IF EXISTS GetWeaponBaseStat;")
    op.execute(
        """
        CREATE PROCEDURE GetWeaponBaseStat(
            IN p_weapon_id INT,
            IN p_stat_id VARCHAR(255)
        )
        BEGIN
            SELECT * FROM weapon_base_stat
            WHERE weapon_id = p_weapon_id
            AND stat_id = p_stat_id;
        END
        """
    )

    op.execute("DROP PROCEDURE IF EXISTS AddWeaponBaseStat;")
    op.execute(
        """
        CREATE PROCEDURE AddWeaponBaseStat(
            IN p_weapon_id INT,
            IN p_stat_id VARCHAR(255),
            IN p_stat_value INT,
            OUT new_id INT
        )
        BEGIN
            INSERT INTO weapon_base_stat(weapon_id, stat_id, stat_value)
            VALUES (p_weapon_id, p_stat_id, p_stat_value);
            SET new_id = LAST_INSERT_ID();
        END
        """
    )

    op.execute("DROP PROCEDURE IF EXISTS UpdateWeaponBaseStat;")
    op.execute(
        """
        CREATE PROCEDURE UpdateWeaponBaseStat(
            IN p_id INT,
            IN p_weapon_id INT,
            IN p_stat_id VARCHAR(255),
            IN p_stat_value INT
        )
        BEGIN
            UPDATE weapon_base_stat
            SET weapon_id = p_weapon_id,
                stat_id = p_stat_id,
                stat_value = p_stat_value
            WHERE id = p_id;
        END
        """
    )


def downgrade() -> None:
    op.execute("DROP PROCEDURE IF EXISTS UpdateWeaponBaseStat;")
    op.execute("DROP PROCEDURE IF EXISTS AddWeaponBaseStat;")
    op.execute("DROP PROCEDURE IF EXISTS GetWeaponBaseStat;")

    op.execute("DROP PROCEDURE IF EXISTS UpdateWeapon;")
    op.execute("DROP PROCEDURE IF EXISTS AddWeapon;")
    op.execute("DROP PROCEDURE IF EXISTS GetWeapon;")
    # Suppression de la table des statistiques de base
    op.drop_table('weapon_base_stat')
    # Suppression de la table principale "weapon"
    op.drop_table('weapon')

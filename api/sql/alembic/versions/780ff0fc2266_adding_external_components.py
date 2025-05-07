"""adding external components

Revision ID: 780ff0fc2266
Revises: eedfb118a616
Create Date: 2025-05-06 18:50:33.402244

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '780ff0fc2266'
down_revision: Union[str, None] = 'eedfb118a616'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ────────── TABLE PRINCIPALE ──────────
    op.create_table(
        'external_component',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('external_component_name_id', sa.Integer,
                  sa.ForeignKey('translation_strings.id'), nullable=False),
        sa.Column('external_component_id', sa.Integer, nullable=False, unique=True),
        sa.Column('image_url', sa.String(255), nullable=True),
        sa.Column('equipment_type', sa.Integer,
                  sa.ForeignKey('translation_strings.id'), nullable=True),
        sa.Column('external_component_tier_id', sa.String(255), nullable=True)
    )

    # ────────── BASE‑STAT ──────────
    op.create_table(
        'external_component_base_stat',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('external_component_id', sa.Integer,
                  sa.ForeignKey('external_component.external_component_id'), nullable=False),
        sa.Column('level', sa.Integer, nullable=False),
        sa.Column('stat_id', sa.Integer,
                  sa.ForeignKey('translation_strings.id'), nullable=False),
        sa.Column('stat_value', sa.Integer, nullable=False)
    )

    # ────────── SET‑OPTION ──────────
    op.create_table(
        'external_component_set_option',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('external_component_id', sa.Integer,
                  sa.ForeignKey('external_component.external_component_id'), nullable=False),
        sa.Column('set_option', sa.Integer,
                  sa.ForeignKey('translation_strings.id'), nullable=False),
        sa.Column('set_count', sa.Integer, nullable=False),
        sa.Column('set_option_effect', sa.Integer,
                  sa.ForeignKey('translation_strings.id'), nullable=False)
    )

    # ────────── STORED PROCEDURES ──────────
    # ---- ExternalComponent ----
    op.execute("DROP PROCEDURE IF EXISTS GetExternalComponent;")
    op.execute(
        """
        CREATE PROCEDURE GetExternalComponent(
            IN p_external_component_id INT
        )
        BEGIN
            SELECT * FROM external_component
            WHERE external_component_id = p_external_component_id;
        END
        """
    )

    op.execute("DROP PROCEDURE IF EXISTS AddExternalComponent;")
    op.execute(
        """
        CREATE PROCEDURE AddExternalComponent(
            IN p_ext_comp_name_id INT,
            IN p_ext_comp_id INT,
            IN p_image_url VARCHAR(255),
            IN p_equipment_type_id INT,
            IN p_ext_comp_tier_id VARCHAR(255),
            OUT new_id INT
        )
        BEGIN
            INSERT INTO external_component(
                external_component_name_id,
                external_component_id,
                image_url,
                equipment_type,
                external_component_tier_id
            )
            VALUES (
                p_ext_comp_name_id,
                p_ext_comp_id,
                p_image_url,
                p_equipment_type_id,
                p_ext_comp_tier_id
            );
            SET new_id = LAST_INSERT_ID();
        END
        """
    )

    op.execute("DROP PROCEDURE IF EXISTS UpdateExternalComponent;")
    op.execute(
        """
        CREATE PROCEDURE UpdateExternalComponent(
            IN p_id INT,
            IN p_ext_comp_name_id INT,
            IN p_ext_comp_id INT,
            IN p_image_url VARCHAR(255),
            IN p_equipment_type_id INT,
            IN p_ext_comp_tier_id VARCHAR(255)
        )
        BEGIN
            UPDATE external_component
            SET external_component_name_id = p_ext_comp_name_id,
                external_component_id      = p_ext_comp_id,
                image_url                  = p_image_url,
                equipment_type             = p_equipment_type_id,
                external_component_tier_id = p_ext_comp_tier_id
            WHERE id = p_id;
        END
        """
    )

    # ---- BaseStat ----
    op.execute("DROP PROCEDURE IF EXISTS GetExternalComponentBaseStat;")
    op.execute(
        """
        CREATE PROCEDURE GetExternalComponentBaseStat(
            IN p_ext_comp_id INT,
            IN p_stat_id INT,
            IN p_level INT
        )
        BEGIN
            SELECT * FROM external_component_base_stat
            WHERE external_component_id = p_ext_comp_id
              AND stat_id               = p_stat_id
              AND level                 = p_level;
        END
        """
    )

    op.execute("DROP PROCEDURE IF EXISTS AddExternalComponentBaseStat;")
    op.execute(
        """
        CREATE PROCEDURE AddExternalComponentBaseStat(
            IN p_ext_comp_id INT,
            IN p_level INT,
            IN p_stat_id INT,
            IN p_stat_value INT,
            OUT new_id INT
        )
        BEGIN
            INSERT INTO external_component_base_stat(
                external_component_id, level, stat_id, stat_value
            )
            VALUES (p_ext_comp_id, p_level, p_stat_id, p_stat_value);
            SET new_id = LAST_INSERT_ID();
        END
        """
    )

    op.execute("DROP PROCEDURE IF EXISTS UpdateExternalComponentBaseStat;")
    op.execute(
        """
        CREATE PROCEDURE UpdateExternalComponentBaseStat(
            IN p_id INT,
            IN p_ext_comp_id INT,
            IN p_level INT,
            IN p_stat_id INT,
            IN p_stat_value INT
        )
        BEGIN
            UPDATE external_component_base_stat
            SET external_component_id = p_ext_comp_id,
                level                 = p_level,
                stat_id               = p_stat_id,
                stat_value            = p_stat_value
            WHERE id = p_id;
        END
        """
    )

    # ---- SetOption ----
    op.execute("DROP PROCEDURE IF EXISTS GetExternalComponentSetOption;")
    op.execute(
        """
        CREATE PROCEDURE GetExternalComponentSetOption(
            IN p_ext_comp_id INT,
            IN p_set_option_id INT
        )
        BEGIN
            SELECT * FROM external_component_set_option
            WHERE external_component_id = p_ext_comp_id
              AND set_option           = p_set_option_id;
        END
        """
    )

    op.execute("DROP PROCEDURE IF EXISTS AddExternalComponentSetOption;")
    op.execute(
        """
        CREATE PROCEDURE AddExternalComponentSetOption(
            IN p_ext_comp_id INT,
            IN p_set_option_id INT,
            IN p_set_count INT,
            IN p_set_option_effect_id INT,
            OUT new_id INT
        )
        BEGIN
            INSERT INTO external_component_set_option(
                external_component_id, set_option, set_count, set_option_effect
            )
            VALUES (p_ext_comp_id, p_set_option_id, p_set_count, p_set_option_effect_id);
            SET new_id = LAST_INSERT_ID();
        END
        """
    )

    op.execute("DROP PROCEDURE IF EXISTS UpdateExternalComponentSetOption;")
    op.execute(
        """
        CREATE PROCEDURE UpdateExternalComponentSetOption(
            IN p_id INT,
            IN p_ext_comp_id INT,
            IN p_set_option_id INT,
            IN p_set_count INT,
            IN p_set_option_effect_id INT
        )
        BEGIN
            UPDATE external_component_set_option
            SET external_component_id = p_ext_comp_id,
                set_option            = p_set_option_id,
                set_count             = p_set_count,
                set_option_effect     = p_set_option_effect_id
            WHERE id = p_id;
        END
        """
    )


# ════════════════════════════════════════════════════
#                      DOWNGRADE
# ════════════════════════════════════════════════════
def downgrade() -> None:
    # Procédures
    op.execute("DROP PROCEDURE IF EXISTS UpdateExternalComponentSetOption;")
    op.execute("DROP PROCEDURE IF EXISTS AddExternalComponentSetOption;")
    op.execute("DROP PROCEDURE IF EXISTS GetExternalComponentSetOption;")

    op.execute("DROP PROCEDURE IF EXISTS UpdateExternalComponentBaseStat;")
    op.execute("DROP PROCEDURE IF EXISTS AddExternalComponentBaseStat;")
    op.execute("DROP PROCEDURE IF EXISTS GetExternalComponentBaseStat;")

    op.execute("DROP PROCEDURE IF EXISTS UpdateExternalComponent;")
    op.execute("DROP PROCEDURE IF EXISTS AddExternalComponent;")
    op.execute("DROP PROCEDURE IF EXISTS GetExternalComponent;")

    # Tables
    op.drop_table('external_component_set_option')
    op.drop_table('external_component_base_stat')
    op.drop_table('external_component')

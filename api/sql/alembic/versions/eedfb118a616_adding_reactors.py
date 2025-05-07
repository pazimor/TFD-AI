"""adding reactors

Revision ID: eedfb118a616
Revises: 922731919809
Create Date: 2025-04-23 21:05:23.423589

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eedfb118a616'
down_revision: Union[str, None] = '922731919809'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # ---------- table principale reactor ----------
    op.create_table(
        'reactor',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('reactor_name_id', sa.Integer, sa.ForeignKey('translation_strings.id'), nullable=False),
        sa.Column('reactor_id', sa.Integer, nullable=False, unique=True),
        sa.Column('image_url', sa.String(255), nullable=True),
        sa.Column('reactor_tier_id', sa.String(255), nullable=True),
        sa.Column('optimized_condition_type', sa.Integer, sa.ForeignKey('translation_strings.id'), nullable=True)
    )

    # ---------- reactor_skill_power ----------
    op.create_table(
        'reactor_skill_power',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('reactor_id', sa.Integer, sa.ForeignKey('reactor.reactor_id'), nullable=False),
        sa.Column('level', sa.Integer, nullable=False),
        sa.Column('skill_atk_power', sa.Integer, nullable=False),
        sa.Column('sub_skill_atk_power', sa.Integer, nullable=False),
        sa.UniqueConstraint('reactor_id', 'level', name='uix_reactor_lvl')
    )

    # ---------- coefficients ----------
    op.create_table(
        'reactor_coeff',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('reactor_id', sa.Integer, sa.ForeignKey('reactor.reactor_id'), nullable=False),
        sa.Column('level', sa.Integer, nullable=False),
        sa.Column('coeff_stat_id', sa.Integer, sa.ForeignKey('translation_strings.id'), nullable=False),
        sa.Column('coeff_stat_value', sa.Float, nullable=False),
        sa.UniqueConstraint('reactor_id', 'level', 'coeff_stat_id', name='uix_reactor_coeff')
    )

    # ---------- enchant effects ----------
    op.create_table(
        'reactor_enchant',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('reactor_id', sa.Integer, sa.ForeignKey('reactor.reactor_id'), nullable=False),
        sa.Column('level', sa.Integer, nullable=False),
        sa.Column('enchant_level', sa.Integer, nullable=False),
        sa.Column('stat_id', sa.Integer, sa.ForeignKey('translation_strings.id'), nullable=False),
        sa.Column('value', sa.Integer, nullable=False),
        sa.UniqueConstraint('reactor_id', 'level', 'enchant_level', 'stat_id', name='uix_reactor_enchant')
    )

    # --------- Stored procedures ----------
    # Reactor
    op.execute("DROP PROCEDURE IF EXISTS GetReactor;")
    op.execute("""
        CREATE PROCEDURE GetReactor(IN p_reactor_id INT)
        BEGIN
            SELECT * FROM reactor WHERE reactor_id = p_reactor_id;
        END
    """)

    op.execute("DROP PROCEDURE IF EXISTS AddReactor;")
    op.execute("""
        CREATE PROCEDURE AddReactor(
            IN p_reactor_name_id INT,
            IN p_reactor_id INT,
            IN p_image_url VARCHAR(255),
            IN p_reactor_tier_id VARCHAR(255),
            IN p_optimized_condition_type INT,
            OUT new_id INT
        )
        BEGIN
            INSERT INTO reactor(
                reactor_name_id, reactor_id, image_url,
                reactor_tier_id, optimized_condition_type
            )
            VALUES (
                p_reactor_name_id, p_reactor_id, p_image_url,
                p_reactor_tier_id, p_optimized_condition_type
            );
            SET new_id = LAST_INSERT_ID();
        END
    """)

    op.execute("DROP PROCEDURE IF EXISTS UpdateReactor;")
    op.execute("""
        CREATE PROCEDURE UpdateReactor(
            IN p_id INT,
            IN p_reactor_name_id INT,
            IN p_reactor_id INT,
            IN p_image_url VARCHAR(255),
            IN p_reactor_tier_id VARCHAR(255),
            IN p_optimized_condition_type INT
        )
        BEGIN
            UPDATE reactor
            SET reactor_name_id = p_reactor_name_id,
                reactor_id = p_reactor_id,
                image_url = p_image_url,
                reactor_tier_id = p_reactor_tier_id,
                optimized_condition_type = p_optimized_condition_type
            WHERE id = p_id;
        END
    """)

    # Reactor Skill Power
    for proc in (
        ("GetReactorSkillPower", """
            CREATE PROCEDURE GetReactorSkillPower(
                IN p_reactor_id INT, IN p_level INT
            )
            BEGIN
                SELECT * FROM reactor_skill_power
                WHERE reactor_id = p_reactor_id AND level = p_level;
            END
        """),
        ("AddReactorSkillPower", """
            CREATE PROCEDURE AddReactorSkillPower(
                IN p_reactor_id INT,
                IN p_level INT,
                IN p_skill_atk_power INT,
                IN p_sub_skill_atk_power INT,
                OUT new_id INT
            )
            BEGIN
                INSERT INTO reactor_skill_power(
                    reactor_id, level, skill_atk_power, sub_skill_atk_power
                ) VALUES (
                    p_reactor_id, p_level, p_skill_atk_power, p_sub_skill_atk_power
                );
                SET new_id = LAST_INSERT_ID();
            END
        """),
        ("UpdateReactorSkillPower", """
            CREATE PROCEDURE UpdateReactorSkillPower(
                IN p_id INT,
                IN p_reactor_id INT,
                IN p_level INT,
                IN p_skill_atk_power INT,
                IN p_sub_skill_atk_power INT
            )
            BEGIN
                UPDATE reactor_skill_power
                SET reactor_id = p_reactor_id,
                    level = p_level,
                    skill_atk_power = p_skill_atk_power,
                    sub_skill_atk_power = p_sub_skill_atk_power
                WHERE id = p_id;
            END
        """),
        ("GetReactorCoeff", """
            CREATE PROCEDURE GetReactorCoeff(
                IN p_reactor_id INT, IN p_level INT, IN p_coeff_stat_id INT
            )
            BEGIN
                SELECT * FROM reactor_coeff
                WHERE reactor_id = p_reactor_id
                  AND level = p_level
                  AND coeff_stat_id = p_coeff_stat_id;
            END
        """),
        ("AddReactorCoeff", """
            CREATE PROCEDURE AddReactorCoeff(
                IN p_reactor_id INT,
                IN p_level INT,
                IN p_coeff_stat_id INT,
                IN p_coeff_stat_value FLOAT,
                OUT new_id INT
            )
            BEGIN
                INSERT INTO reactor_coeff(
                    reactor_id, level, coeff_stat_id, coeff_stat_value
                ) VALUES (
                    p_reactor_id, p_level, p_coeff_stat_id, p_coeff_stat_value
                );
                SET new_id = LAST_INSERT_ID();
            END
        """),
        ("UpdateReactorCoeff", """
            CREATE PROCEDURE UpdateReactorCoeff(
                IN p_id INT,
                IN p_reactor_id INT,
                IN p_level INT,
                IN p_coeff_stat_id INT,
                IN p_coeff_stat_value FLOAT
            )
            BEGIN
                UPDATE reactor_coeff
                SET reactor_id = p_reactor_id,
                    level = p_level,
                    coeff_stat_id = p_coeff_stat_id,
                    coeff_stat_value = p_coeff_stat_value
                WHERE id = p_id;
            END
        """),
        ("GetReactorEnchant", """
            CREATE PROCEDURE GetReactorEnchant(
                IN p_reactor_id INT, IN p_level INT, IN p_enchant_level INT, IN p_stat_id INT
            )
            BEGIN
                SELECT * FROM reactor_enchant
                WHERE reactor_id = p_reactor_id
                  AND level = p_level
                  AND enchant_level = p_enchant_level
                  AND stat_id = p_stat_id;
            END
        """),
        ("AddReactorEnchant", """
            CREATE PROCEDURE AddReactorEnchant(
                IN p_reactor_id INT,
                IN p_level INT,
                IN p_enchant_level INT,
                IN p_stat_id INT,
                IN p_value INT,
                OUT new_id INT
            )
            BEGIN
                INSERT INTO reactor_enchant(
                    reactor_id, level, enchant_level, stat_id, value
                ) VALUES (
                    p_reactor_id, p_level, p_enchant_level, p_stat_id, p_value
                );
                SET new_id = LAST_INSERT_ID();
            END
        """),
        ("UpdateReactorEnchant", """
            CREATE PROCEDURE UpdateReactorEnchant(
                IN p_id INT,
                IN p_reactor_id INT,
                IN p_level INT,
                IN p_enchant_level INT,
                IN p_stat_id INT,
                IN p_value INT
            )
            BEGIN
                UPDATE reactor_enchant
                SET reactor_id = p_reactor_id,
                    level = p_level,
                    enchant_level = p_enchant_level,
                    stat_id = p_stat_id,
                    value = p_value
                WHERE id = p_id;
            END
        """)
    ):
        op.execute(f"DROP PROCEDURE IF EXISTS {proc[0]};")
        op.execute(proc[1])


def downgrade() -> None:
    # drop procedures
    for proc in (
        "UpdateReactorEnchant", "AddReactorEnchant", "GetReactorEnchant",
        "UpdateReactorCoeff", "AddReactorCoeff", "GetReactorCoeff",
        "UpdateReactorSkillPower", "AddReactorSkillPower", "GetReactorSkillPower",
        "UpdateReactor", "AddReactor", "GetReactor"
    ):
        op.execute(f"DROP PROCEDURE IF EXISTS {proc};")

    # drop tables
    op.drop_table('reactor_enchant')
    op.drop_table('reactor_coeff')
    op.drop_table('reactor_skill_power')
    op.drop_table('reactor')
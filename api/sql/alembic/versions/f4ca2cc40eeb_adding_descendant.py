"""adding descendant

Revision ID: f4ca2cc40eeb
Revises: de219f4ba144
Create Date: 2025-04-17 18:11:32.696547

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f4ca2cc40eeb'
down_revision: Union[str, None] = 'de219f4ba144'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'descendant',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('descendant_id', sa.Integer, nullable=False, unique=True),
        sa.Column('descendant_name', sa.Integer,
                  sa.ForeignKey('translation_strings.id'), nullable=False),
        sa.Column('descendant_group_id', sa.Integer, nullable=False),
        sa.Column('descendant_image_url', sa.String(512), nullable=False)
    )

    op.create_table(
        'descendant_stat',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('descendant_id', sa.Integer,
                  sa.ForeignKey('descendant.descendant_id'), nullable=False),
        sa.Column('level', sa.Integer, nullable=False)
    )

    op.create_table(
        'descendant_stat_detail',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('descendant_id', sa.Integer,
                  sa.ForeignKey('descendant.descendant_id'), nullable=False),
        sa.Column('level', sa.Integer, nullable=False),
        sa.Column('stat_id', sa.Integer, nullable=False),
        sa.Column('stat_value', sa.Float, nullable=False)
    )

    op.create_table(
        'descendant_skill',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('descendant_id', sa.Integer,
                  sa.ForeignKey('descendant.descendant_id'), nullable=False),
        sa.Column('skill_type', sa.Integer,
                  sa.ForeignKey('translation_strings.id'), nullable=False),
        sa.Column('skill_name', sa.Integer,
                  sa.ForeignKey('translation_strings.id'), nullable=False),
        sa.Column('element_type', sa.Integer,
                  sa.ForeignKey('translation_strings.id'), nullable=False),
        sa.Column('arche_type', sa.Integer,
                  sa.ForeignKey('translation_strings.id'), nullable=True),
        sa.Column('skill_image_url', sa.String(512), nullable=False),
        sa.Column('skill_description', sa.Integer,
                  sa.ForeignKey('translation_strings.id'), nullable=False)
    )

    op.execute("DROP PROCEDURE IF EXISTS GetDescendant;")
    op.execute(
        """
        CREATE PROCEDURE GetDescendant(IN p_descendant_id INT)
        BEGIN
            SELECT * FROM descendant WHERE descendant_id = p_descendant_id;
        END
        """)

    op.execute("DROP PROCEDURE IF EXISTS AddDescendant;")
    op.execute(
        """
        CREATE PROCEDURE AddDescendant(
            IN p_descendant_id INT,
            IN p_descendant_name INT,
            IN p_descendant_group_id INT,
            IN p_descendant_image_url VARCHAR(512),
            OUT new_id INT
        )
        BEGIN
            INSERT INTO descendant(
                descendant_id, descendant_name,
                descendant_group_id, descendant_image_url)
            VALUES (p_descendant_id, p_descendant_name,
                    p_descendant_group_id, p_descendant_image_url);
            SET new_id = LAST_INSERT_ID();
        END
        """)

    op.execute("DROP PROCEDURE IF EXISTS UpdateDescendant;")
    op.execute(
        """
        CREATE PROCEDURE UpdateDescendant(
            IN p_id INT,
            IN p_descendant_id INT,
            IN p_descendant_name INT,
            IN p_descendant_group_id INT,
            IN p_descendant_image_url VARCHAR(512)
        )
        BEGIN
            UPDATE descendant
            SET descendant_id        = p_descendant_id,
                descendant_name      = p_descendant_name,
                descendant_group_id  = p_descendant_group_id,
                descendant_image_url = p_descendant_image_url
            WHERE id = p_id;
        END
        """)

    op.execute("DROP PROCEDURE IF EXISTS GetDescendantStat;")
    op.execute(
        """
        CREATE PROCEDURE GetDescendantStat(
            IN p_descendant_id INT,
            IN p_level INT
        )
        BEGIN
            SELECT * FROM descendant_stat
            WHERE descendant_id = p_descendant_id AND level = p_level;
        END
        """)

    op.execute("DROP PROCEDURE IF EXISTS AddDescendantStat;")
    op.execute(
        """
        CREATE PROCEDURE AddDescendantStat(
            IN p_descendant_id INT,
            IN p_level INT,
            OUT new_id INT
        )
        BEGIN
            INSERT INTO descendant_stat(descendant_id, level)
            VALUES (p_descendant_id, p_level);
            SET new_id = LAST_INSERT_ID();
        END
        """)

    op.execute("DROP PROCEDURE IF EXISTS UpdateDescendantStat;")
    op.execute(
        """
        CREATE PROCEDURE UpdateDescendantStat(
            IN p_id INT,
            IN p_descendant_id INT,
            IN p_level INT
        )
        BEGIN
            UPDATE descendant_stat
            SET descendant_id = p_descendant_id,
                level         = p_level
            WHERE id = p_id;
        END
        """)

    op.execute("DROP PROCEDURE IF EXISTS GetDescendantStatDetail;")
    op.execute(
        """
        CREATE PROCEDURE GetDescendantStatDetail(
            IN p_descendant_id INT,
            IN p_level INT,
            IN p_stat_id INT
        )
        BEGIN
            SELECT * FROM descendant_stat_detail
            WHERE descendant_id = p_descendant_id
              AND level         = p_level
              AND stat_id       = p_stat_id;
        END
        """)

    op.execute("DROP PROCEDURE IF EXISTS AddDescendantStatDetail;")
    op.execute(
        """
        CREATE PROCEDURE AddDescendantStatDetail(
            IN p_descendant_id INT,
            IN p_level INT,
            IN p_stat_id INT,
            IN p_stat_value FLOAT,
            OUT new_id INT
        )
        BEGIN
            INSERT INTO descendant_stat_detail(
                descendant_id, level, stat_id, stat_value)
            VALUES (p_descendant_id, p_level, p_stat_id, p_stat_value);
            SET new_id = LAST_INSERT_ID();
        END
        """)

    op.execute("DROP PROCEDURE IF EXISTS UpdateDescendantStatDetail;")
    op.execute(
        """
        CREATE PROCEDURE UpdateDescendantStatDetail(
            IN p_id INT,
            IN p_descendant_id INT,
            IN p_level INT,
            IN p_stat_id INT,
            IN p_stat_value FLOAT
        )
        BEGIN
            UPDATE descendant_stat_detail
            SET descendant_id = p_descendant_id,
                level         = p_level,
                stat_id       = p_stat_id,
                stat_value    = p_stat_value
            WHERE id = p_id;
        END
        """)

    op.execute("DROP PROCEDURE IF EXISTS GetDescendantSkill;")
    op.execute(
        """
        CREATE PROCEDURE GetDescendantSkill(
            IN p_descendant_id INT,
            IN p_skill_name INT
        )
        BEGIN
            SELECT * FROM descendant_skill
            WHERE descendant_id = p_descendant_id
              AND skill_name    = p_skill_name;
        END
        """)

    op.execute("DROP PROCEDURE IF EXISTS AddDescendantSkill;")
    op.execute(
        """
        CREATE PROCEDURE AddDescendantSkill(
            IN p_descendant_id INT,
            IN p_skill_type INT,
            IN p_skill_name INT,
            IN p_element_type INT,
            IN p_arche_type INT,
            IN p_skill_image_url VARCHAR(512),
            IN p_skill_description INT,
            OUT new_id INT
        )
        BEGIN
            INSERT INTO descendant_skill(
                descendant_id, skill_type, skill_name,
                element_type, arche_type,
                skill_image_url, skill_description)
            VALUES (p_descendant_id, p_skill_type, p_skill_name,
                    p_element_type, p_arche_type,
                    p_skill_image_url, p_skill_description);
            SET new_id = LAST_INSERT_ID();
        END
        """)

    op.execute("DROP PROCEDURE IF EXISTS UpdateDescendantSkill;")
    op.execute(
        """
        CREATE PROCEDURE UpdateDescendantSkill(
            IN p_id INT,
            IN p_descendant_id INT,
            IN p_skill_type INT,
            IN p_skill_name INT,
            IN p_element_type INT,
            IN p_arche_type INT,
            IN p_skill_image_url VARCHAR(512),
            IN p_skill_description INT
        )
        BEGIN
            UPDATE descendant_skill
            SET descendant_id     = p_descendant_id,
                skill_type        = p_skill_type,
                skill_name        = p_skill_name,
                element_type      = p_element_type,
                arche_type        = p_arche_type,
                skill_image_url   = p_skill_image_url,
                skill_description = p_skill_description
            WHERE id = p_id;
        END
        """)


def downgrade() -> None:
    for proc in (
        "UpdateDescendantSkill", "AddDescendantSkill", "GetDescendantSkill",
        "UpdateDescendantStatDetail", "AddDescendantStatDetail", "GetDescendantStatDetail",
        "UpdateDescendantStat", "AddDescendantStat", "GetDescendantStat",
        "UpdateDescendant", "AddDescendant", "GetDescendant"):
        op.execute(f"DROP PROCEDURE IF EXISTS {proc};")

    op.drop_table('descendant_skill')
    op.drop_table('descendant_stat_detail')
    op.drop_table('descendant_stat')
    op.drop_table('descendant')

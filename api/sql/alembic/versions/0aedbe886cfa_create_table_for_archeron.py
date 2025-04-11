"""Create table for archeron

Revision ID: 0aedbe886cfa
Revises: 80617b5e11ab
Create Date: 2025-03-23 14:12:48.584735

"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0aedbe886cfa'
down_revision: Union[str, None] = '80617b5e11ab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Table pour gérer les traductions multi-langues
    op.create_table(
        'translation_strings',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('fr', sa.Text, nullable=True),
        sa.Column('ko', sa.Text, nullable=True),
        sa.Column('en', sa.Text, nullable=True),
        sa.Column('de', sa.Text, nullable=True),
        sa.Column('ja', sa.Text, nullable=True),
        sa.Column('zh_cn', sa.Text, nullable=True),
        sa.Column('zh_tw', sa.Text, nullable=True),
        sa.Column('it', sa.Text, nullable=True),
        sa.Column('pl', sa.Text, nullable=True),
        sa.Column('pt', sa.Text, nullable=True),
        sa.Column('ru', sa.Text, nullable=True),
        sa.Column('es', sa.Text, nullable=True)
    )

    # Table pour stocker les boards (arbre de compétences)
    op.create_table(
        'boards',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('arche_tuning_board_id', sa.Integer, unique=True, nullable=False),
        sa.Column('row_size', sa.Integer, nullable=False),
        sa.Column('column_size', sa.Integer, nullable=False),
    )

    # Table pour stocker les nœuds de l'arbre
    op.create_table(
        'nodes',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('node_id', sa.Integer, unique=True, nullable=False),
        sa.Column('name_id', sa.Integer, nullable=False),
        sa.Column('image_url', sa.Text, nullable=True),
        sa.Column('node_type', sa.String(50), nullable=True),
        sa.Column('tier_id', sa.String(50), nullable=True),
        sa.Column('required_tuning_point', sa.Integer, nullable=True),
    )

    # Table pour stocker les effets/statistiques des nœuds
    op.create_table(
        'node_effects',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('node_id', sa.Integer, sa.ForeignKey('nodes.node_id'), nullable=False),
        sa.Column('stat_id', sa.Integer, nullable=False),
        sa.Column('stat_value', sa.Integer, nullable=False),
        sa.Column('operator_type', sa.String(10), nullable=False),
    )

    # Table pour lier un board à ses nœuds et stocker leur position
    op.create_table(
        'board_nodes',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('board_id', sa.Integer, sa.ForeignKey('boards.id'), nullable=False),
        sa.Column('node_id', sa.Integer, sa.ForeignKey('nodes.node_id'), nullable=False),
        sa.Column('position_row', sa.Integer, nullable=False),
        sa.Column('position_column', sa.Integer, nullable=False),
    )

    # Table pour la hiérarchie entre boards
    op.create_table(
        'board_groups',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('arche_tuning_board_group_id', sa.String(255), nullable=False),
        sa.Column('descendant_group_id', sa.String(255), nullable=False),
        sa.Column('board_id', sa.Integer, sa.ForeignKey('boards.arche_tuning_board_id'), nullable=True),
    )

    op.execute("DROP PROCEDURE IF EXISTS UpdateTranslation;")
    op.execute("""
            CREATE PROCEDURE UpdateTranslation(
                IN p_language_id INTEGER,
                IN p_language_fr TEXT,
                IN p_language_ko TEXT,
                IN p_language_en TEXT,
                IN p_language_de TEXT,
                IN p_language_ja TEXT,
                IN p_language_zh_cn TEXT,
                IN p_language_zh_tw TEXT,
                IN p_language_it TEXT,
                IN p_language_pl TEXT,
                IN p_language_pt TEXT,
                IN p_language_ru TEXT,
                IN p_language_es TEXT
            )
            BEGIN
                UPDATE translation_strings
                SET
                    fr = p_language_fr,
                    ko = p_language_ko,
                    en = p_language_en,
                    de = p_language_de,
                    ja = p_language_ja,
                    zh_cn = p_language_zh_cn,
                    zh_tw = p_language_zh_tw,
                    it = p_language_it,
                    pl = p_language_pl,
                    pt = p_language_pt,
                    ru = p_language_ru,
                    es = p_language_es
                WHERE id = p_language_id;
            END;
            """)

    op.execute("DROP PROCEDURE IF EXISTS AddTranslation;")
    op.execute("""
        
        CREATE PROCEDURE AddTranslation(
            IN p_language_fr TEXT,
            IN p_language_ko TEXT,
            IN p_language_en TEXT,
            IN p_language_de TEXT,
            IN p_language_ja TEXT,
            IN p_language_zh_cn TEXT,
            IN p_language_zh_tw TEXT,
            IN p_language_it TEXT,
            IN p_language_pl TEXT,
            IN p_language_pt TEXT,
            IN p_language_ru TEXT,
            IN p_language_es TEXT
        )
        BEGIN
            INSERT INTO translation_strings (fr, ko, en, de, ja, zh_cn, zh_tw, it, pl, pt, ru, es)
            VALUES (p_language_fr, p_language_ko, p_language_en, p_language_de, p_language_ja, p_language_zh_cn, p_language_zh_tw, p_language_it, p_language_pl, p_language_pt, p_language_ru, p_language_es );
            SELECT LAST_INSERT_ID() AS inserted_id;
        END;
        """)

    op.execute("DROP PROCEDURE IF EXISTS GetTranslation;")
    op.execute("""
                CREATE PROCEDURE GetTranslation(IN p_language_id INTEGER)
                BEGIN
                    SELECT * FROM translation_strings WHERE id = p_language_id;
                END;
                """)

    op.execute("DROP PROCEDURE IF EXISTS FindTranslation;")
    op.execute("""
                    CREATE PROCEDURE FindTranslation(
                        IN p_language_column VARCHAR(10),
                        IN p_search_text TEXT
                    )
                    BEGIN
                        SET @query = CONCAT(
                            'SELECT id FROM translation_strings WHERE ', 
                            p_language_column, 
                            ' = ? LIMIT 1'
                        );
                        
                        SET @search_text = p_search_text;

                        PREPARE stmt FROM @query;
                        EXECUTE stmt USING @search_text;
                        DEALLOCATE PREPARE stmt;
                    END;
                    """)

    op.execute("DROP PROCEDURE IF EXISTS UpdateBoardGroups;")
    op.execute("""
                    CREATE PROCEDURE UpdateBoardGroups(
                        IN p_id INTEGER,
                        IN p_arche_tuning_board_group_id TEXT,
                        IN p_descendant_group_id TEXT,
                        IN p_board_id TEXT
                    )
                    BEGIN
                        UPDATE board_groups
                        SET
                            arche_tuning_board_group_id = p_arche_tuning_board_group_id,
                            descendant_group_id = p_descendant_group_id,
                            board_id = board_id
                        WHERE id = p_lboard_group_id;
                    END;
                    """)

    op.execute("DROP PROCEDURE IF EXISTS AddBoardGroups;")
    op.execute("""

                CREATE PROCEDURE AddBoardGroups(
                    IN p_id INTEGER,
                    IN p_arche_tuning_board_group_id TEXT,
                    IN p_descendant_group_id TEXT,
                    IN p_board_id TEXT
                )
                BEGIN
                    INSERT INTO board_groups (id, arche_tuning_board_group_id, descendant_group_id, board_id)
                    VALUES (p_id, p_arche_tuning_board_group_id, p_descendant_group_id, p_board_id);
                END;
                """)



def downgrade() -> None:
    op.drop_table('board_groups')
    op.drop_table('board_nodes')
    op.drop_table('node_effects')
    op.drop_table('nodes')
    op.drop_table('boards')
    op.drop_table('translation_strings')

    op.execute("DROP PROCEDURE IF EXISTS GetTranslation;")
    op.execute("DROP PROCEDURE IF EXISTS UpdateTranslation;")
    op.execute("DROP PROCEDURE IF EXISTS addTranslation;")
    op.execute("DROP PROCEDURE IF EXISTS UpdateBoardGroups;")
    op.execute("DROP PROCEDURE IF EXISTS AddBoardGroups;")
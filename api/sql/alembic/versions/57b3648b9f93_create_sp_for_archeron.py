"""Create SP for archeron

Revision ID: 57b3648b9f93
Revises: 0aedbe886cfa
Create Date: 2025-04-05 17:12:43.294351

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '57b3648b9f93'
down_revision: Union[str, None] = '0aedbe886cfa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # node_effects - UPSERT
    op.execute("DROP PROCEDURE IF EXISTS UpsertNodeEffects;")
    op.execute("""
    CREATE PROCEDURE UpsertNodeEffects(
        IN p_id INT,
        IN p_node_id INT,
        IN p_stat_id VARCHAR(255),
        IN p_stat_value INT,
        IN p_operator_type VARCHAR(10)
    )
    BEGIN
        IF p_id IS NOT NULL AND EXISTS (SELECT id FROM node_effects WHERE id = p_id) THEN
            UPDATE node_effects SET
                node_id = p_node_id,
                stat_id = p_stat_id,
                stat_value = p_stat_value,
                operator_type = p_operator_type
            WHERE id = p_id;
            SELECT p_id AS affected_id;
        ELSE
            INSERT INTO node_effects (node_id, stat_id, stat_value, operator_type)
            VALUES (p_node_id, p_stat_id, p_stat_value, p_operator_type);
            SELECT LAST_INSERT_ID() AS affected_id;
        END IF;
    END;
    """)

    # nodes - UPSERT
    op.execute("DROP PROCEDURE IF EXISTS UpsertNodes;")
    op.execute("""
    CREATE PROCEDURE UpsertNodes(
        IN p_node_id VARCHAR(255),
        IN p_name_id INT,
        IN p_image_url TEXT,
        IN p_node_type VARCHAR(50),
        IN p_tier_id VARCHAR(50),
        IN p_required_tuning_point INT
    )
    BEGIN
        IF EXISTS (SELECT id FROM nodes WHERE node_id = p_node_id) THEN
            UPDATE nodes SET
                name_id = p_name_id,
                image_url = p_image_url,
                node_type = p_node_type,
                tier_id = p_tier_id,
                required_tuning_point = p_required_tuning_point
            WHERE node_id = p_node_id;
    
            SELECT id FROM nodes WHERE node_id = p_node_id;
        ELSE
            INSERT INTO nodes (node_id, name_id, image_url, node_type, tier_id, required_tuning_point)
            VALUES (p_node_id, p_name_id, p_image_url, p_node_type, p_tier_id, p_required_tuning_point);
    
            SELECT LAST_INSERT_ID();
        END IF;
    END;
    """)

    # boards - UPSERT
    op.execute("DROP PROCEDURE IF EXISTS UpsertBoards;")
    op.execute("""
        CREATE PROCEDURE UpsertBoards(
            IN p_arche_tuning_board_id VARCHAR(255),
            IN p_row_size INT,
            IN p_column_size INT
        )
        BEGIN
            IF EXISTS (SELECT id FROM boards WHERE arche_tuning_board_id = p_arche_tuning_board_id) THEN
                UPDATE boards
                SET row_size = p_row_size, column_size = p_column_size
                WHERE arche_tuning_board_id = p_arche_tuning_board_id;

                SELECT id AS board_id FROM boards WHERE arche_tuning_board_id = p_arche_tuning_board_id;
            ELSE
                INSERT INTO boards (arche_tuning_board_id, row_size, column_size)
                VALUES (p_arche_tuning_board_id, p_row_size, p_column_size);

                SELECT LAST_INSERT_ID() AS board_id;
            END IF;
        END;
        """)

    # board_nodes - UPSERT
    op.execute("DROP PROCEDURE IF EXISTS UpsertBoardNodes;")
    op.execute("""
    CREATE PROCEDURE UpsertBoardNodes(
        IN p_id INT,
        IN p_board_id INT,
        IN p_node_id INT,
        IN p_position_row INT,
        IN p_position_column INT
    )
    BEGIN
        IF p_id IS NOT NULL AND EXISTS (SELECT id FROM board_nodes WHERE id = p_id) THEN
            UPDATE board_nodes SET
                board_id = p_board_id,
                node_id = p_node_id,
                position_row = p_position_row,
                position_column = p_position_column
            WHERE id = p_id;
            SELECT p_id AS affected_id;
        ELSE
            INSERT INTO board_nodes (board_id, node_id, position_row, position_column)
            VALUES (p_board_id, p_node_id, p_position_row, p_position_column);
            SELECT LAST_INSERT_ID() AS affected_id;
        END IF;
    END;
    """)

    op.execute("DROP PROCEDURE IF EXISTS UpsertBoardGroups;")
    op.execute("""
        CREATE PROCEDURE UpsertBoardGroups(
            IN p_id INTEGER,
            IN p_arche_tuning_board_group_id TEXT,
            IN p_descendant_group_id TEXT,
            IN p_board_id TEXT
        )
        BEGIN
            IF p_id IS NOT NULL AND EXISTS (SELECT id FROM board_groups WHERE id = p_id) THEN
                UPDATE board_groups
                SET
                    arche_tuning_board_group_id = p_arche_tuning_board_group_id,
                    descendant_group_id = p_descendant_group_id,
                    board_id = p_board_id
                WHERE id = p_id;
                SELECT p_id AS affected_id;
            ELSE
                INSERT INTO board_groups (id, arche_tuning_board_group_id, descendant_group_id, board_id)
                VALUES (p_id, p_arche_tuning_board_group_id, p_descendant_group_id, p_board_id);
                SELECT p_id AS affected_id;
            END IF;
        END;
        """)

    op.execute("DROP PROCEDURE IF EXISTS GetNodesByID;")
    op.execute("""
    CREATE PROCEDURE GetNodesByID(IN p_node_id VARCHAR(255))
    BEGIN
        SELECT id FROM nodes WHERE node_id = p_node_id;
    END;
    """)

    op.execute("DROP PROCEDURE IF EXISTS UpsertTranslation;")
    op.execute("""
    CREATE PROCEDURE UpsertTranslation(
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
        IF p_language_id = 0 THEN
            INSERT INTO translation_strings (
                fr, ko, en, de, ja, zh_cn, zh_tw, it, pl, pt, ru, es
            )
            VALUES (
                p_language_fr, p_language_ko, p_language_en, p_language_de, p_language_ja,
                p_language_zh_cn, p_language_zh_tw, p_language_it, p_language_pl,
                p_language_pt, p_language_ru, p_language_es
            );
            SELECT LAST_INSERT_ID() AS inserted_id;
        ELSE
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
            SELECT p_language_id AS affected_id;
        END IF;
    END;
    """)


def downgrade() -> None:
    ## too be sure (no residues)
    op.execute("DROP PROCEDURE IF EXISTS UpdateBoardNodes;")
    op.execute("DROP PROCEDURE IF EXISTS AddBoardNodes;")
    op.execute("DROP PROCEDURE IF EXISTS UpdateBoards;")
    op.execute("DROP PROCEDURE IF EXISTS AddBoards;")
    op.execute("DROP PROCEDURE IF EXISTS UpdateNodes;")
    op.execute("DROP PROCEDURE IF EXISTS AddNodes;")
    op.execute("DROP PROCEDURE IF EXISTS UpdateNodeEffects;")
    op.execute("DROP PROCEDURE IF EXISTS AddNodeEffects;")
    op.execute("DROP PROCEDURE IF EXISTS UpdateBoardGroups;")
    op.execute("DROP PROCEDURE IF EXISTS AddBoardGroups;")
    op.execute("DROP PROCEDURE IF EXISTS GetNodesByID;")

    op.execute("DROP PROCEDURE IF EXISTS UpsertBoardNodes;")
    op.execute("DROP PROCEDURE IF EXISTS UpsertBoards;")
    op.execute("DROP PROCEDURE IF EXISTS UpsertNodes;")
    op.execute("DROP PROCEDURE IF EXISTS UpsertNodeEffects;")
    op.execute("DROP PROCEDURE IF EXISTS UpsertBoardGroups;")
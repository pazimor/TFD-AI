"""setup builds

Revision ID: bd774a63875b
Revises: 0798e41b422d
Create Date: 2025-06-11 09:40:58.430738

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bd774a63875b'
down_revision: Union[str, None] = '0798e41b422d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("DROP PROCEDURE IF EXISTS AddUserBuild;")
    op.execute("""
    CREATE PROCEDURE AddUserBuild(
        IN p_user_id VARCHAR(255),
        IN p_build_name VARCHAR(255),
        IN p_build_data JSON
    )
    BEGIN
        INSERT INTO user_builds(user_id, build_name, build_data)
        VALUES(p_user_id, p_build_name, p_build_data);
        SELECT LAST_INSERT_ID() AS build_id;
    END;
    """)

    # Procédure de mise à jour
    op.execute("DROP PROCEDURE IF EXISTS UpdateUserBuild;")
    op.execute("""
    CREATE PROCEDURE UpdateUserBuild(
        IN p_build_id INT,
        IN p_user_id VARCHAR(255),
        IN p_build_name VARCHAR(255),
        IN p_build_data JSON
    )
    BEGIN
        UPDATE user_builds
        SET build_name = p_build_name,
            build_data = p_build_data,
            updated_at = NOW()
        WHERE
            build_id = p_build_id
        AND
            user_id = p_user_id;
        SELECT ROW_COUNT()
        AS affected;
    END;
    """)

    # Procédure de récupération par utilisateur
    op.execute("DROP PROCEDURE IF EXISTS GetUserBuilds;")
    op.execute("""
    CREATE PROCEDURE GetUserBuilds(
        IN p_user_id VARCHAR(255)
    )
    BEGIN
        SELECT * FROM user_builds
        WHERE user_id = p_user_id
        ORDER BY created_at;
    END;
    """)

    # Procédure de récupération unique
    op.execute("DROP PROCEDURE IF EXISTS GetUserBuild;")
    op.execute("""
    CREATE PROCEDURE GetUserBuild(
        IN p_build_id INT
    )
    BEGIN
        SELECT * FROM user_builds
        WHERE build_id = p_build_id;
    END;
    """)


def downgrade() -> None:
    op.execute("DROP PROCEDURE IF EXISTS AddUserBuild;")
    op.execute("DROP PROCEDURE IF EXISTS UpdateUserBuild;")
    op.execute("DROP PROCEDURE IF EXISTS GetUserBuilds;")
    op.execute("DROP PROCEDURE IF EXISTS GetUserBuild;")

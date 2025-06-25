"""add user photo blob

Revision ID: d55ba4ba8bb4
Revises: f4ca2cc40eeb
Create Date: 2025-11-14 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '88aa99d757d5'
down_revision: Union[str, None] = 'bd774a63875b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.add_column('users', sa.Column('photo_data', sa.LargeBinary(), nullable=True))
    op.drop_column('users', 'photo_url')
    op.execute("DROP PROCEDURE IF EXISTS SyncUser;")
    op.execute(
        '''
        CREATE PROCEDURE SyncUser(
            IN p_id VARCHAR(255),
            IN p_name VARCHAR(255),
            IN p_email VARCHAR(255),
            IN p_photo LONGBLOB
        )
        BEGIN
        INSERT INTO users (id, name, email, photo_data)
        VALUES (
                   p_id,
                   p_name,
                   AES_ENCRYPT(p_email, 'your_secret_key'),
                   p_photo
               )
            ON DUPLICATE KEY UPDATE
                                 name = VALUES(name),
                                 email = AES_ENCRYPT(p_email, 'your_secret_key'),
                                 photo_data = VALUES(photo_data);
        END
        '''
    )
    op.execute("DROP PROCEDURE IF EXISTS GetUserPhoto;")
    op.execute(
        '''
        CREATE PROCEDURE GetUserPhoto(IN p_user_id VARCHAR(255))
        BEGIN
        SELECT photo_data FROM users WHERE id = p_user_id;
        END
        '''
    )

    op.execute("DROP PROCEDURE IF EXISTS GetAllReactors;")
    op.execute(
        '''
        CREATE PROCEDURE GetAllReactors()
        BEGIN
            WITH
            stats AS (
                SELECT
                    rc.reactor_id,
                    JSON_ARRAYAGG(
                        JSON_OBJECT(
                            'level',      rc.level,
                            'stat_id',    rc.coeff_stat_id,
                            'stat_value', rc.coeff_stat_value
                        )
                    ) AS stats_json
                FROM reactor_coeff rc
                WHERE rc.level = 100
                GROUP BY rc.reactor_id
            ),
            coeff AS (
                SELECT
                    rc.reactor_id,
                    JSON_ARRAYAGG(
                        JSON_OBJECT(
                            'coeff_stat_id',    rc.coeff_stat_id,
                            'coeff_stat_value', rc.coeff_stat_value
                        )
                    ) AS coeff_json
                FROM reactor_coeff rc
                WHERE rc.level = 100
                GROUP BY rc.reactor_id
            ),
            enchant AS (
                SELECT
                    re.reactor_id,
                    JSON_ARRAYAGG(
                        JSON_OBJECT(
                            'enchant_level', re.enchant_level,
                            'stat_id',       re.stat_id,
                            'value',         re.value
                        )
                        ORDER BY re.enchant_level
                    ) AS enchant_json
                FROM reactor_enchant re
                WHERE re.level = 100
                GROUP BY re.reactor_id
            ),
            skill AS (
                SELECT
                    rsp.reactor_id,
                    JSON_ARRAYAGG(
                        JSON_OBJECT(
                            'level',              rsp.level,
                            'skill_atk_power',    rsp.skill_atk_power,
                            'sub_skill_atk_power', rsp.sub_skill_atk_power,
                            'coefficient',       CAST(COALESCE(c.coeff_json, JSON_ARRAY()) AS JSON),
                            'enchant_effect',    CAST(COALESCE(e.enchant_json, JSON_ARRAY()) AS JSON)
                        )
                    ) AS skill_power_json
                FROM reactor_skill_power rsp
                LEFT JOIN coeff   c ON c.reactor_id = rsp.reactor_id
                LEFT JOIN enchant e ON e.reactor_id = rsp.reactor_id
                WHERE rsp.level = 100
                GROUP BY rsp.reactor_id
            )
            SELECT
                r.id,
                r.reactor_id,
                r.reactor_name_id,
                r.optimized_condition_type AS equipment_type_id,
                r.image_url,
                r.reactor_tier_id,

                COALESCE(s.stats_json,  JSON_ARRAY()) AS base_stat,
                COALESCE(sk.skill_power_json, JSON_ARRAY()) AS skill_power
            FROM reactor r
                LEFT JOIN stats s ON s.reactor_id = r.reactor_id
                LEFT JOIN skill sk ON sk.reactor_id = r.reactor_id
            ORDER BY r.reactor_id;
        END
        '''
    )


def downgrade() -> None:
    op.execute("DROP PROCEDURE IF EXISTS GetUserPhoto;")
    op.execute("DROP PROCEDURE IF EXISTS SyncUser;")
    op.execute("DROP PROCEDURE IF EXISTS GetAllReactors;")
    op.add_column('users', sa.Column('photo_url', sa.String(length=255), nullable=True))
    op.drop_column('users', 'photo_data')

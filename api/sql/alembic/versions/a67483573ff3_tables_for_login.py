"""Tables for Login

Revision ID: a67483573ff3
Revises: 780ff0fc2266
Create Date: 2025-05-10 17:28:50.291924

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a67483573ff3'
down_revision: Union[str, None] = '780ff0fc2266'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.String(255), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('email', sa.LargeBinary, nullable=False),  # AES_ENCRYPT
        sa.Column('photo_url', sa.String(255), nullable=True)
    )

    op.create_table(
        'user_settings',
        sa.Column('user_id', sa.String(255), sa.ForeignKey('users.id'), primary_key=True),
        sa.Column('default_language', sa.String(10), nullable=True)
    )

    op.execute("DROP PROCEDURE IF EXISTS SyncUser;")
    op.execute(
        '''
        CREATE PROCEDURE SyncUser(
            IN p_id VARCHAR(255),
            IN p_name VARCHAR(255),
            IN p_email VARCHAR(255),
            IN p_photo_url VARCHAR(255)
        )
        BEGIN
            INSERT INTO users (id, name, email, photo_url)
            VALUES (
                p_id,
                p_name,
                AES_ENCRYPT(p_email, 'your_secret_key'),
                p_photo_url
            )
            ON DUPLICATE KEY UPDATE
                name = VALUES(name),
                email = AES_ENCRYPT(p_email, 'your_secret_key'),
                photo_url = VALUES(photo_url);
        END
        '''
    )

    op.execute(
        '''
        CREATE PROCEDURE GetUserSettings(IN p_user_id VARCHAR(255))
        BEGIN
            SELECT * FROM user_settings WHERE user_id = p_user_id;
        END
        '''
    )

    # Drop and (re)create SetUserSettings procedure
    op.execute("DROP PROCEDURE IF EXISTS SetUserSettings;")
    op.execute(
        '''
        CREATE PROCEDURE SetUserSettings(
            IN p_user_id VARCHAR(255),
            IN p_default_language VARCHAR(10)
        )
        BEGIN
            INSERT INTO user_settings (user_id, default_language)
            VALUES (p_user_id, p_default_language)
            ON DUPLICATE KEY UPDATE
                default_language = VALUES(default_language);
        END
        '''
    )
def downgrade() -> None:
    op.execute("DROP PROCEDURE IF EXISTS SyncUser;")
    op.execute("DROP PROCEDURE IF EXISTS GetUserSettings;")
    op.execute("DROP PROCEDURE IF EXISTS SetUserSettings;")
    op.drop_table('user_settings')
    op.drop_table('users')

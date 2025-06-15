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


def downgrade() -> None:
    op.execute("DROP PROCEDURE IF EXISTS GetUserPhoto;")
    op.execute("DROP PROCEDURE IF EXISTS SyncUser;")
    op.add_column('users', sa.Column('photo_url', sa.String(length=255), nullable=True))
    op.drop_column('users', 'photo_data')

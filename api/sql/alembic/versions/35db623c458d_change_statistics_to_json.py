"""change_statistics_to_json

Revision ID: 35db623c458d
Revises: ae60b1a4d8cf
Create Date: 2025-02-23 00:54:09.395857

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '35db623c458d'
down_revision: Union[str, None] = 'ae60b1a4d8cf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('modifiers') as batch_op:
        op.execute("DROP PROCEDURE IF EXISTS AddModifier;")
        op.execute("DROP PROCEDURE IF EXISTS UpdateModifier;")

        # Suppression de drop_constraint car aucune contrainte JSON existante
        batch_op.alter_column(
            'modifier_statistiques',
            type_=sa.JSON,
            existing_type=sa.String(1024),
            existing_nullable=True
        )

        # Ajout d'une nouvelle contrainte CHECK pour valider le JSON
        batch_op.create_check_constraint(
            'modifier_statistiques_json_check',
            sa.text("JSON_VALID(modifier_statistiques)")
        )

        op.execute("""
                CREATE PROCEDURE AddModifier(
                    IN p_modifier_id INTEGER,
                    IN p_modifier_name JSON,
                    IN p_modifier_type VARCHAR(150),
                    IN p_modifier_statistiques JSON,
                    IN p_modifier_stack_id VARCHAR(50),
                    IN p_modifier_stack_description JSON,
                    in p_modifier_displaydata JSON
                )
                BEGIN
                    INSERT INTO modifiers (modifier_id, modifier_name, modifier_type, modifier_statistiques, modifier_stack_id, modifier_stack_description, modifier_displaydata)
                    VALUES (p_modifier_id, p_modifier_name, p_modifier_type, p_modifier_statistiques, p_modifier_stack_id, p_modifier_stack_description, p_modifier_displaydata);
                END;
                """)

        op.execute("""
                CREATE PROCEDURE UpdateModifier(
                    IN p_modifier_id INTEGER,
                    IN p_modifier_name JSON,
                    IN p_modifier_type VARCHAR(150),
                    IN p_modifier_statistiques JSON,
                    IN p_modifier_stack_id VARCHAR(50),
                    IN p_modifier_stack_description JSON,
                    in p_modifier_displaydata JSON
                )
                BEGIN
                    UPDATE modifiers
                    SET 
                        modifier_name = p_modifier_name,
                        modifier_type = p_modifier_type,
                        modifier_statistiques = p_modifier_statistiques,
                        modifier_stack_id = p_modifier_stack_id,
                        modifier_stack_description = p_modifier_stack_description,
                        modifier_displaydata = p_modifier_displaydata
                    WHERE p_modifier_id = modifier_id;
                END;
                """)




def downgrade() -> None:
    with op.batch_alter_table('modifiers') as batch_op:
        # Suppression de la contrainte JSON ajoutée lors de l'upgrade
        batch_op.drop_constraint('modifier_statistiques_json_check', type_='check')

        op.execute("DROP PROCEDURE IF EXISTS AddModifier;")
        op.execute("DROP PROCEDURE IF EXISTS UpdateModifier;")

        # Retour à une colonne VARCHAR(1024)
        batch_op.alter_column(
            'modifier_statistiques',
            existing_type=sa.JSON,
            type_=sa.String(1024),
            existing_nullable=True
        )
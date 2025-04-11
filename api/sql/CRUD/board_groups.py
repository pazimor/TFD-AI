from sql.database import SessionLocal
from sqlalchemy import text

# ================================
# CRUD for BOARDS_GROUPS
# ================================

session = SessionLocal()

def upsert_board_groups(p_id, arche_tuning_board_group_id, descendant_group_id, board_id):
    try:
        result = session.execute(
            text("CALL UpsertBoardGroups(:p_id, :arche_tuning_board_group_id, :descendant_group_id, :board_id)"),
            {
                "p_id": p_id,
                "arche_tuning_board_group_id": arche_tuning_board_group_id,
                "descendant_group_id": descendant_group_id,
                "board_id": board_id
            }
        )
        affected_id = result.fetchone()[0]
        session.commit()
        return affected_id
    except Exception as e:
        print(f"❌ Erreur : {e}")
        session.rollback()
        return None
    finally:
        pass
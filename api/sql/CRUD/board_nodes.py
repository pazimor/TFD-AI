from sql.database import SessionLocal
from sqlalchemy import text

# ================================
# CRUD for BOARDS_NODES
# ================================

session = SessionLocal()

def upsert_board_nodes(p_id, p_board_id, p_node_id, p_position_row, p_position_column):
    try:
        result = session.execute(
            text("CALL UpsertBoardNodes(:p_id, :p_board_id, :p_node_id, :p_position_row, :p_position_column)"),
            {
                "p_id": p_id,
                "p_board_id": p_board_id,
                "p_node_id": p_node_id,
                "p_position_row": p_position_row,
                "p_position_column": p_position_column
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
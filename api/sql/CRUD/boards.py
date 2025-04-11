from sql.database import SessionLocal
from sqlalchemy import text

# ================================
# CRUD for BOARDS
# ================================

session = SessionLocal()

def upsert_boards(arche_tuning_board_id, row_size, column_size):
    try:
        result = session.execute(
            text("CALL UpsertBoards(:arche_tuning_board_id, :row_size, :column_size)"),
            {
                "arche_tuning_board_id": arche_tuning_board_id,
                "row_size": row_size,
                "column_size": column_size
            }
        )
        board_id = result.fetchone()[0]
        session.commit()
        return board_id
    except Exception as e:
        print(f"❌ Erreur : {e}")
        session.rollback()
        return None
    finally:
        pass
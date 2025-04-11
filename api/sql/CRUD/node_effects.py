from sql.database import SessionLocal
from sqlalchemy import text

# ================================
# CRUD for NODE_EFFECTS
# ================================
session = SessionLocal()

def upsert_node_effects(p_id=None, node_id=None, stat_id=None, stat_value=None, operator_type=None):
    try:
        result = session.execute(
            text("CALL UpsertNodeEffects(:p_id, :node_id, :stat_id, :stat_value, :operator_type)"),
            {
                "p_id": p_id,
                "node_id": node_id,
                "stat_id": stat_id,
                "stat_value": stat_value,
                "operator_type": operator_type,
            }
        )
        new_id = result.fetchone()[0]
        session.commit()
        return new_id
    except Exception as e:
        print(f"❌ Erreur : {e}")
        session.rollback()
        return None
    finally:
        pass
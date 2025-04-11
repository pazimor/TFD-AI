from sql.database import SessionLocal
from sqlalchemy import text


# ================================
# CRUD for NODES
# ================================

session = SessionLocal()

def upsert_nodes(node_id, name_id, image_url, node_type, tier_id, required_tuning_point):
    try:
        result = session.execute(
            text("CALL UpsertNodes(:node_id, :name_id, :image_url, :node_type, :tier_id, :required_tuning_point)"),
            {
                "node_id": node_id,
                "name_id": name_id,
                "image_url": image_url,
                "node_type": node_type,
                "tier_id": tier_id,
                "required_tuning_point": required_tuning_point
            }
        )
        real_node_id = result.fetchone()[0]
        session.commit()
        return real_node_id
    except Exception as e:
        print(f"❌ Erreur : {e}")
        session.rollback()
        return None
    finally:
        pass

def get_nodes_by_id(node_external_id):
    try:
        result = session.execute(
            text("CALL GetNodesByID(:node_id)"),
            {"node_id": node_external_id}
        ).fetchone()

        return result[0] if result else -1
    except Exception as e:
        print(f"❌ Erreur lors du SELECT : {e}")
        session.rollback()
        return None
    finally:
        pass
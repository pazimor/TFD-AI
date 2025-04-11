import json

from sql.database import SessionLocal
from sqlalchemy import text

session = SessionLocal()

# ================================
# CRUD for ITEMS
# ================================
def add_item(id, name, item_type, goals, capabilities, stats, display_json):
    try:
        session.execute(
            text("CALL AddItem(:id, :name, :type, :goals, :capabilities, :statistiques, :displaydata)"),
            {
                "id": id,
                "name": name,
                "type": item_type,
                "goals": goals,
                "capabilities": capabilities,
                "statistiques": stats,
                "displaydata": display_json
            }
        )
        session.commit()
    except Exception as e:
        print(f"❌ Erreur : {e}")
        session.rollback()
    finally:
        pass

def get_item(id):
    try:
        result = session.execute(text("CALL GetItem(:id)", {"id": id}))
        item = result.fetchone()
        return item
    except Exception as e:
        print(f"❌ Erreur : {e}")
    finally:
        pass

def get_items_by_type(item_type):
    try:
        result = session.execute(
            text("CALL GetItemsByType(:type)"),
            {"type": item_type}
        )
        modifiers = result.fetchall()
        return modifiers
    except Exception as e:
        print(f"❌ Erreur : {e}")
    finally:
        pass

def update_item(id, name, goals, item_type, capabilities, stats, display_json):
    try:
        session.execute(
            text("CALL UpdateItem(:id, :name, :goals, :type, :capabilities, :statistiques, :displaydata)"),
            {
                "id": id,
                "name": name,
                "goals": goals,
                "type": item_type,
                "capabilities": capabilities,
                "statistiques": stats,
                "displaydata": display_json
            }
        )
        session.commit()
    except Exception as e:
        print(f"❌ Erreur : {e}")
        session.rollback()
    finally:
        pass

def delete_item(id):
    try:
        session.execute(text("CALL DeleteItem(:id)", {"id": id}))
        session.commit()
    except Exception as e:
        print(f"❌ Erreur : {e}")
        session.rollback()
    finally:
        pass

# ================================
# send ITEMS
# ================================

def add_items(item):
    try:
        existing = session.execute(
            text("CALL GetItem(:id)"),
            {"id": item["id"]}
        ).fetchone()

        name_json = json.dumps(item["name"], ensure_ascii=False)
        capabilities_json = json.dumps(item["capabilities"], ensure_ascii=False) if item["capabilities"] is not None else None
        statistics_json = json.dumps(item["statistics"], ensure_ascii=False)
        display_json = json.dumps(item["displaydata"], ensure_ascii=False)

        if not existing:
            add_item(item["id"], name_json, item["type"], item["goals"], capabilities_json,
                          statistics_json, display_json)
        else:
            update_item(item["id"], name_json, item["type"], item["goals"], capabilities_json,
                             statistics_json, display_json)
    except Exception as e:
        print(f"❌ Erreur lors de l'ajout/mise à jour de l'item '{item['name']}': {e}")
        session.rollback()
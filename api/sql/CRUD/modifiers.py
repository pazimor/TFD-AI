import json

from sql.database import SessionLocal
from sqlalchemy import text

session = SessionLocal()

# ================================
# CRUD pour MODIFIERS
# ================================
def add_modifier(id, name, modifier_type, stats, stack_id, stack_description, displaydata):
    try:
        session.execute(
            text("CALL AddModifier(:id, :name, :type, :stats, :stack_id, :stack_description, :displaydata)"),
            {
                "id": id,
                "name": name,
                "type": modifier_type,
                "stats": stats,
                "stack_id": stack_id,
                "stack_description": stack_description,
                "displaydata": displaydata
            }
        )
        session.commit()
    except Exception as e:
        print(f"❌ Erreur lors de la récupération du modifier {id}: {e}")
        session.rollback()
    finally:
        pass

def update_modifier(id, name, modifier_type, stats, stack_id, stack_description, displaydata):
    try:
        session.execute(
            text("CALL UpdateModifier(:id, :name, :type, :stats, :stack_id, :stack_description, :displaydata)"),
            {
                "id": id,
                "name": name,
                "type": modifier_type,
                "stats": stats,
                "stack_id": stack_id,
                "stack_description": stack_description,
                "displaydata": displaydata
            }
        )
        session.commit()
    except Exception as e:
        print(f"❌ Erreur lors de l'update du modifier {id}: {e}")
        session.rollback()
    finally:
        pass

def get_modifier(modifier_id):
    try:
        query = text("CALL GetModifier(:id)")  # On s'assure que le paramètre correspond bien
        result = session.execute(query, {"id": modifier_id})  # Nom du paramètre bien cohérent
        modifier = result.fetchone()
        return modifier
    except Exception as e:
        print(f"❌ Erreur lors de la récupération du modifier {modifier_id}: {e}")
    finally:
        pass

def get_modifiers_by_type(modifier_type):
    try:
        result = session.execute(
            text("CALL GetModifiersByType(:type)"),
            {"type": modifier_type}
        )
        modifiers = result.fetchall()
        return modifiers
    except Exception as e:
        print(f"❌ Erreur : {e}")
    finally:
        pass


def add_modifiers(modifier):
    """Ajoute ou met à jour un modifier en base de données en utilisant les procédures stockées."""
    try:
        existing = session.execute(
            text("CALL GetModifier(:id)"),
            {"id": modifier["id"]}
        ).fetchone()

        display_json = json.dumps(modifier["displaydata"], ensure_ascii=False)
        name = json.dumps(modifier["name"], ensure_ascii=False)
        statistics = json.dumps(modifier["statistics"], ensure_ascii=False)

        if not existing:
            add_modifier(modifier["id"], name, modifier["type"], statistics, modifier["stack_id"], modifier["stack_description"], display_json)
        else:
            update_modifier(modifier["id"], name, modifier["type"], statistics, modifier["stack_id"], modifier["stack_description"], display_json)
    except Exception as e:
        print(f"❌ Erreur lors de l'ajout/mise à jour du modifier '{modifier['name']}': {e}")
        session.rollback()
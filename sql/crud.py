# crud.py
from sql.database import SessionLocal
from sqlalchemy import text

# ================================
# CRUD pour ITEMS
# ================================
def add_item(id, name, item_type, goals, capabilities, stats, display_json):
    session = SessionLocal()
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
        session.close()

def get_item(id):
    session = SessionLocal()
    try:
        result = session.execute(text("CALL GetItem(:id)", {"id": id}))
        item = result.fetchone()
        return item
    except Exception as e:
        print(f"❌ Erreur : {e}")
    finally:
        session.close()

def get_items_by_type(item_type):
    session = SessionLocal()
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
        session.close()

def update_item(id, name, goals, item_type, capabilities, stats, display_json):
    session = SessionLocal()
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
        session.close()

def delete_item(id):
    session = SessionLocal()
    try:
        session.execute(text("CALL DeleteItem(:id)", {"id": id}))
        session.commit()
    except Exception as e:
        print(f"❌ Erreur : {e}")
        session.rollback()
    finally:
        session.close()


# ================================
# CRUD pour MODIFIERS
# ================================
def add_modifier(id, name, modifier_type, stats, stack_id, stack_description, displaydata):
    session = SessionLocal()
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
        session.close()

def update_modifier(id, name, modifier_type, stats, stack_id, stack_description, displaydata):
    session = SessionLocal()
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
        session.close()

def get_modifier(modifier_id):
    session = SessionLocal()
    try:
        query = text("CALL GetModifier(:id)")  # On s'assure que le paramètre correspond bien
        result = session.execute(query, {"id": modifier_id})  # Nom du paramètre bien cohérent
        modifier = result.fetchone()
        return modifier
    except Exception as e:
        print(f"❌ Erreur lors de la récupération du modifier {modifier_id}: {e}")
    finally:
        session.close()

def get_modifiers_by_type(modifier_type):
    session = SessionLocal()
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
        session.close()


# ================================
# CRUD pour BUILDS
# ================================
def add_build(build_name, item_id, score_per_goal):
    session = SessionLocal()
    try:
        session.execute(
            "CALL AddBuild(:build_name, :item_id, :score_per_goal)",
            {"build_name": build_name, "item_id": item_id, "score_per_goal": score_per_goal}
        )
        session.commit()
        print("✅ Build ajouté avec succès!")
    except Exception as e:
        print(f"❌ Erreur : {e}")
        session.rollback()
    finally:
        session.close()

def get_build(build_id):
    session = SessionLocal()
    try:
        result = session.execute("CALL GetBuild(:build_id)", {"build_id": build_id})
        build = result.fetchone()
        return build
    except Exception as e:
        print(f"❌ Erreur : {e}")
    finally:
        session.close()


# ================================
# CRUD pour BUILD_MODIFIERS
# ================================
def add_build_modifier(build_id, modifier_id, quantity):
    session = SessionLocal()
    try:
        session.execute(
            "CALL AddBuildModifier(:build_id, :modifier_id, :quantity)",
            {"build_id": build_id, "modifier_id": modifier_id, "quantity": quantity}
        )
        session.commit()
        print("✅ Modifier ajouté au build avec succès!")
    except Exception as e:
        print(f"❌ Erreur : {e}")
        session.rollback()
    finally:
        session.close()

def get_build_modifiers(build_id):
    session = SessionLocal()
    try:
        result = session.execute("CALL GetBuildModifiers(:build_id)", {"build_id": build_id})
        modifiers = result.fetchall()
        return modifiers
    except Exception as e:
        print(f"❌ Erreur : {e}")
    finally:
        session.close()

def delete_build_modifiers(build_id):
    session = SessionLocal()
    try:
        session.execute("CALL DeleteBuildModifiers(:build_id)", {"build_id": build_id})
        session.commit()
        print("✅ Tous les modifiers du build ont été supprimés!")
    except Exception as e:
        print(f"❌ Erreur : {e}")
        session.rollback()
    finally:
        session.close()
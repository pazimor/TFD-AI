# crud.py
from sql.database import SessionLocal
from sqlalchemy import text


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
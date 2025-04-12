from sql.database import SessionLocal
from sqlalchemy import text

# ================================
# CRUD for weapon_base_stat
# ================================

def get_weapon_base_stat(weapon_id, stat_id):
    session = SessionLocal()
    try:
        result = session.execute(
            text("CALL GetWeaponBaseStat(:p_weapon_id, :p_stat_id)"),
            {"p_weapon_id": weapon_id, "p_stat_id": stat_id}
        )
        row = result.fetchone()
        session.commit()
        return row[1] if row else None
    except Exception as e:
        print(f"❌ Erreur dans get_weapon_base_stat: {e}")
        session.rollback()
        return None

def add_weapon_base_stat(weapon_id, stat_id, stat_value):
    session = SessionLocal()
    try:
        # Appel de la procédure stockée AddWeaponBaseStat avec le paramètre OUT via la variable @new_id
        session.execute(
            text("CALL AddWeaponBaseStat(:p_weapon_id, :p_stat_id, :p_stat_value, @new_id)"),
            {
                "p_weapon_id": weapon_id,
                "p_stat_id": stat_id,
                "p_stat_value": stat_value
            }
        )
        # Récupération de l'ID nouvellement inséré via la variable de session @new_id
        new_id_result = session.execute(text("SELECT @new_id")).fetchone()
        session.commit()
        return new_id_result[0] if new_id_result else None
    except Exception as e:
        print(f"❌ Erreur dans add_weapon_base_stat: {e}")
        session.rollback()
        return None

def update_weapon_base_stat(id, weapon_id, stat_id, stat_value):
    session = SessionLocal()
    try:
        session.execute(
            text("CALL UpdateWeaponBaseStat(:p_id, :p_weapon_id, :p_stat_id, :p_stat_value)"),
            {
                "p_id": id,
                "p_weapon_id": weapon_id,
                "p_stat_id": stat_id,
                "p_stat_value": stat_value
            }
        )
        session.commit()
        return True
    except Exception as e:
        print(f"❌ Erreur dans update_weapon_base_stat: {e}")
        session.rollback()
        return False
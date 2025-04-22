from sql.database import SessionLocal
from sqlalchemy import text

session = SessionLocal()
# =========================================================
# CRUD pour la table module + module_stat
# =========================================================

# ---------- Module ---------------------------------------------------------
def get_module(module_id):
    """Renvoie l’id interne (PK) de la table `module` si elle existe, sinon None."""
    try:
        res = session.execute(
            text("CALL GetModule(:p_module_id)"),
            {"p_module_id": module_id}
        ).fetchone()
        session.commit()
        return res[0] if res else None
    except Exception as e:
        print(f"❌ GetModule : {e}")
        session.rollback()
        return None


def add_module(
    module_name_id, module_id, image_url, module_type, module_tier_id,
    module_socket_type, module_class, available_weapon_type,
    available_descendant_id, available_module_slot_type
):
    try:
        session.execute(
            text(
                """
                CALL AddModule(
                    :p_module_name_id,
                    :p_module_id,
                    :p_image_url,
                    :p_module_type,
                    :p_module_tier_id,
                    :p_module_socket_type,
                    :p_module_class,
                    :p_available_weapon_type,
                    :p_available_descendant_id,
                    :p_available_module_slot_type,
                    @new_id
                )
                """
            ),
            {
                "p_module_name_id": module_name_id,
                "p_module_id": module_id,
                "p_image_url": image_url,
                "p_module_type": module_type,
                "p_module_tier_id": module_tier_id,
                "p_module_socket_type": module_socket_type,
                "p_module_class": module_class,
                "p_available_weapon_type": available_weapon_type,
                "p_available_descendant_id": available_descendant_id,
                "p_available_module_slot_type": available_module_slot_type,
            },
        )
        new_id = session.execute(text("SELECT @new_id")).fetchone()
        session.commit()
        return new_id[0] if new_id else None
    except Exception as e:
        print(f"❌ AddModule : {e}")
        session.rollback()
        return None


def update_module(
    id_db, module_name_id, module_id, image_url, module_type, module_tier_id,
    module_socket_type, module_class, available_weapon_type,
    available_descendant_id, available_module_slot_type
):
    try:
        session.execute(
            text(
                """
                CALL UpdateModule(
                    :p_id,
                    :p_module_name_id,
                    :p_module_id,
                    :p_image_url,
                    :p_module_type,
                    :p_module_tier_id,
                    :p_module_socket_type,
                    :p_module_class,
                    :p_available_weapon_type,
                    :p_available_descendant_id,
                    :p_available_module_slot_type
                )
                """
            ),
            {
                "p_id": id_db,
                "p_module_name_id": module_name_id,
                "p_module_id": module_id,
                "p_image_url": image_url,
                "p_module_type": module_type,
                "p_module_tier_id": module_tier_id,
                "p_module_socket_type": module_socket_type,
                "p_module_class": module_class,
                "p_available_weapon_type": available_weapon_type,
                "p_available_descendant_id": available_descendant_id,
                "p_available_module_slot_type": available_module_slot_type,
            },
        )
        session.commit()
        return True
    except Exception as e:
        print(f"❌ UpdateModule : {e}")
        session.rollback()
        return False


# ---------- Module‑stat ----------------------------------------------------
def get_module_stat(module_id, level):
    """Renvoie l’id interne (PK) du couple (module_id, level) si présent, sinon None."""
    try:
        res = session.execute(
            text("CALL GetModuleStat(:p_module_id, :p_level)"),
            {"p_module_id": module_id, "p_level": level},
        ).fetchone()
        session.commit()
        return res[0] if res else None
    except Exception as e:
        print(f"❌ GetModuleStat : {e}")
        session.rollback()
        return None


def add_module_stat(module_id, level, module_capacity, value):
    try:
        session.execute(
            text(
                """
                CALL AddModuleStat(
                    :p_module_id,
                    :p_level,
                    :p_module_capacity,
                    :p_value,
                    @new_id
                )
                """
            ),
            {
                "p_module_id": module_id,
                "p_level": level,
                "p_module_capacity": module_capacity,
                "p_value": value,
            },
        )
        new_id = session.execute(text("SELECT @new_id")).fetchone()
        session.commit()
        return new_id[0] if new_id else None
    except Exception as e:
        print(f"❌ AddModuleStat : {e}")
        session.rollback()
        return None


def update_module_stat(id_db, module_id, level, module_capacity, value):
    try:
        session.execute(
            text(
                """
                CALL UpdateModuleStat(
                    :p_id,
                    :p_module_id,
                    :p_level,
                    :p_module_capacity,
                    :p_value
                )
                """
            ),
            {
                "p_id": id_db,
                "p_module_id": module_id,
                "p_level": level,
                "p_module_capacity": module_capacity,
                "p_value": value,
            },
        )
        session.commit()
        return True
    except Exception as e:
        print(f"❌ UpdateModuleStat : {e}")
        session.rollback()
        return False
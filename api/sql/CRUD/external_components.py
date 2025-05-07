from sql.database import SessionLocal
from sqlalchemy import text

# =====================================================
# CRUD pour external_component + statistiques & set‑bonus
# =====================================================

session = SessionLocal()


# ────────────────  TABLE PRINCIPALE  ────────────────
def get_external_component(ext_comp_id):
    """
    Retourne l’ID interne (primary key) de la ligne
    correspondant au external_component_id donné,
    ou None si elle n’existe pas.
    """
    try:
        result = session.execute(
            text("CALL GetExternalComponent(:p_external_component_id)"),
            {"p_external_component_id": ext_comp_id}
        )
        row = result.fetchone()
        session.commit()
        # row[0] is the table primary‑key `id`
        return row[0] if row else None
    except Exception as e:
        print(f"❌ Erreur : {e}")
        session.rollback()
        return None


def add_external_component(
    ext_comp_name_id,               # FK translation_strings
    ext_comp_id,                    # business key
    image_url,
    equipment_type_id,              # FK translation_strings
    ext_comp_tier_id
):
    try:
        session.execute(
            text("""
                CALL AddExternalComponent(
                    :p_ext_comp_name_id,
                    :p_ext_comp_id,
                    :p_image_url,
                    :p_equipment_type_id,
                    :p_ext_comp_tier_id,
                    @new_id
                )
            """),
            {
                "p_ext_comp_name_id": ext_comp_name_id,
                "p_ext_comp_id": ext_comp_id,
                "p_image_url": image_url,
                "p_equipment_type_id": equipment_type_id,
                "p_ext_comp_tier_id": ext_comp_tier_id
            }
        )
        new_id = session.execute(text("SELECT @new_id")).fetchone()
        session.commit()
        return new_id[0] if new_id else None
    except Exception as e:
        print(f"❌ Erreur : {e}")
        session.rollback()
        return None


def update_external_component(
    pk_id,                           # id interne (primary key)
    ext_comp_name_id,
    ext_comp_id,
    image_url,
    equipment_type_id,
    ext_comp_tier_id
):
    try:
        session.execute(
            text("""
                CALL UpdateExternalComponent(
                    :p_id,
                    :p_ext_comp_name_id,
                    :p_ext_comp_id,
                    :p_image_url,
                    :p_equipment_type_id,
                    :p_ext_comp_tier_id
                )
            """),
            {
                "p_id": pk_id,
                "p_ext_comp_name_id": ext_comp_name_id,
                "p_ext_comp_id": ext_comp_id,
                "p_image_url": image_url,
                "p_equipment_type_id": equipment_type_id,
                "p_ext_comp_tier_id": ext_comp_tier_id
            }
        )
        session.commit()
        return True
    except Exception as e:
        print(f"❌ Erreur : {e}")
        session.rollback()
        return False


# ────────────────  BASE‑STAT  ────────────────
def get_external_component_base_stat(ext_comp_id, stat_id, level):
    try:
        result = session.execute(
            text("CALL GetExternalComponentBaseStat(:p_ext_comp_id, :p_stat_id, :p_level)"),
            {"p_ext_comp_id": ext_comp_id, "p_stat_id": stat_id, "p_level": level}
        )
        row = result.fetchone()
        session.commit()
        return row[0] if row else None          # primary key
    except Exception as e:
        print(f"❌ Erreur : {e}")
        session.rollback()
        return None


def add_external_component_base_stat(ext_comp_id, level, stat_id, stat_value):
    try:
        session.execute(
            text("""
                CALL AddExternalComponentBaseStat(
                    :p_ext_comp_id,
                    :p_level,
                    :p_stat_id,
                    :p_stat_value,
                    @new_id
                )
            """),
            {
                "p_ext_comp_id": ext_comp_id,
                "p_level": level,
                "p_stat_id": stat_id,
                "p_stat_value": stat_value
            }
        )
        new_id = session.execute(text("SELECT @new_id")).fetchone()
        session.commit()
        return new_id[0] if new_id else None
    except Exception as e:
        print(f"❌ Erreur : {e}")
        session.rollback()
        return None


def update_external_component_base_stat(pk_id, ext_comp_id, level, stat_id, stat_value):
    try:
        session.execute(
            text("""
                CALL UpdateExternalComponentBaseStat(
                    :p_id,
                    :p_ext_comp_id,
                    :p_level,
                    :p_stat_id,
                    :p_stat_value
                )
            """),
            {
                "p_id": pk_id,
                "p_ext_comp_id": ext_comp_id,
                "p_level": level,
                "p_stat_id": stat_id,
                "p_stat_value": stat_value
            }
        )
        session.commit()
        return True
    except Exception as e:
        print(f"❌ Erreur : {e}")
        session.rollback()
        return False


# ────────────────  SET‑OPTION  ────────────────
def get_external_component_set_option(ext_comp_id, set_option_id):
    try:
        result = session.execute(
            text("CALL GetExternalComponentSetOption(:p_ext_comp_id, :p_set_option_id)"),
            {"p_ext_comp_id": ext_comp_id, "p_set_option_id": set_option_id}
        )
        row = result.fetchone()
        session.commit()
        return row[0] if row else None
    except Exception as e:
        print(f"❌ Erreur : {e}")
        session.rollback()
        return None


def add_external_component_set_option(
    ext_comp_id, set_option_id, set_count, set_option_effect_id
):
    try:
        session.execute(
            text("""
                CALL AddExternalComponentSetOption(
                    :p_ext_comp_id,
                    :p_set_option_id,
                    :p_set_count,
                    :p_set_option_effect_id,
                    @new_id
                )
            """),
            {
                "p_ext_comp_id": ext_comp_id,
                "p_set_option_id": set_option_id,
                "p_set_count": set_count,
                "p_set_option_effect_id": set_option_effect_id
            }
        )
        new_id = session.execute(text("SELECT @new_id")).fetchone()
        session.commit()
        return new_id[0] if new_id else None
    except Exception as e:
        print(f"❌ Erreur : {e}")
        session.rollback()
        return None


def update_external_component_set_option(
    pk_id, ext_comp_id, set_option_id, set_count, set_option_effect_id
):
    try:
        session.execute(
            text("""
                CALL UpdateExternalComponentSetOption(
                    :p_id,
                    :p_ext_comp_id,
                    :p_set_option_id,
                    :p_set_count,
                    :p_set_option_effect_id
                )
            """),
            {
                "p_id": pk_id,
                "p_ext_comp_id": ext_comp_id,
                "p_set_option_id": set_option_id,
                "p_set_count": set_count,
                "p_set_option_effect_id": set_option_effect_id
            }
        )
        session.commit()
        return True
    except Exception as e:
        print(f"❌ Erreur : {e}")
        session.rollback()
        return False
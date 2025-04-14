from sql.database import SessionLocal
from sqlalchemy import text

# ================================
# CRUD for weapon
# ================================

session = SessionLocal()

def get_weapon(weapon_id):
    try:
        result = session.execute(
            text("CALL GetWeapon(:p_weapon_id)"),
            {"p_weapon_id": weapon_id}
        )
        row = result.fetchone()
        session.commit()
        return row[1] if row else None
    except Exception as e:
        print(f"❌ Erreur : {e}")
        session.rollback()
        return None

def add_weapon(
    weapon_name_id, weapon_id, image_url, weapon_type, weapon_tier_id,
    weapon_rounds_type, available_core_slot, weapon_perk_ability_name,
    weapon_perk_ability_description, weapon_perk_ability_image_url,
    firearm_atk_type, firearm_atk_value
):
    try:
        # Appel de la procédure AddWeapon avec le paramètre OUT via la variable @new_id
        session.execute(
            text("""
                CALL AddWeapon(
                    :p_weapon_name_id,
                    :p_weapon_id,
                    :p_image_url,
                    :p_weapon_type,
                    :p_weapon_tier_id,
                    :p_weapon_rounds_type,
                    :p_available_core_slot,
                    :p_weapon_perk_ability_name,
                    :p_weapon_perk_ability_description,
                    :p_weapon_perk_ability_image_url,
                    :p_firearm_atk_type,
                    :p_firearm_atk_value,
                    @new_id
                )
            """),
            {
                "p_weapon_name_id": weapon_name_id,
                "p_weapon_id": weapon_id,
                "p_image_url": image_url,
                "p_weapon_type": weapon_type,
                "p_weapon_tier_id": weapon_tier_id,
                "p_weapon_rounds_type": weapon_rounds_type,
                "p_available_core_slot": available_core_slot,
                "p_weapon_perk_ability_name": weapon_perk_ability_name,
                "p_weapon_perk_ability_description": weapon_perk_ability_description,
                "p_weapon_perk_ability_image_url": weapon_perk_ability_image_url,
                "p_firearm_atk_type": firearm_atk_type,
                "p_firearm_atk_value": firearm_atk_value
            }
        )
        # Récupération de l'ID nouvellement inséré via la variable de session @new_id
        new_id_result = session.execute(text("SELECT @new_id")).fetchone()
        session.commit()
        return new_id_result[0] if new_id_result else None
    except Exception as e:
        print(f"❌ Erreur : {e}")
        session.rollback()
        return None

def update_weapon(
    weapon_id_db, weapon_name_id, weapon_id, image_url, weapon_type, weapon_tier_id,
    weapon_rounds_type, available_core_slot, weapon_perk_ability_name,
    weapon_perk_ability_description, weapon_perk_ability_image_url,
    firearm_atk_type, firearm_atk_value
):
    try:
        session.execute(
            text("""
                CALL UpdateWeapon(
                    :p_id,
                    :p_weapon_name_id,
                    :p_weapon_id,
                    :p_image_url,
                    :p_weapon_type,
                    :p_weapon_tier_id,
                    :p_weapon_rounds_type,
                    :p_available_core_slot,
                    :p_weapon_perk_ability_name,
                    :p_weapon_perk_ability_description,
                    :p_weapon_perk_ability_image_url,
                    :p_firearm_atk_type,
                    :p_firearm_atk_value
                )
            """),
            {
                "p_id": weapon_id_db,
                "p_weapon_name_id": weapon_name_id,
                "p_weapon_id": weapon_id,
                "p_image_url": image_url,
                "p_weapon_type": weapon_type,
                "p_weapon_tier_id": weapon_tier_id,
                "p_weapon_rounds_type": weapon_rounds_type,
                "p_available_core_slot": available_core_slot,
                "p_weapon_perk_ability_name": weapon_perk_ability_name,
                "p_weapon_perk_ability_description": weapon_perk_ability_description,
                "p_weapon_perk_ability_image_url": weapon_perk_ability_image_url,
                "p_firearm_atk_type": firearm_atk_type,
                "p_firearm_atk_value": firearm_atk_value
            }
        )
        session.commit()
        return True
    except Exception as e:
        print(f"❌ Erreur : {e}")
        session.rollback()
        return False
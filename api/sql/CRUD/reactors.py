from sql.database import SessionLocal
from sqlalchemy import text

# ================================
# CRUD principal pour reactor
# ================================
session = SessionLocal()

# ---------- table reactor ----------
def get_reactor(reactor_id):
    try:
        result = session.execute(
            text("CALL GetReactor(:p_reactor_id)"),
            {"p_reactor_id": reactor_id}
        )
        row = result.fetchone()
        session.commit()
        return row[1] if row else None
    except Exception as e:
        print(f"❌ Erreur GetReactor : {e}")
        session.rollback()
        return None


def add_reactor(
    reactor_name_id, reactor_id, image_url, reactor_tier_id,
    optimized_condition_type
):
    try:
        session.execute(
            text("""
                CALL AddReactor(
                    :p_reactor_name_id,
                    :p_reactor_id,
                    :p_image_url,
                    :p_reactor_tier_id,
                    :p_optimized_condition_type,
                    @new_id
                )
            """),
            {
                "p_reactor_name_id": reactor_name_id,
                "p_reactor_id": reactor_id,
                "p_image_url": image_url,
                "p_reactor_tier_id": reactor_tier_id,
                "p_optimized_condition_type": optimized_condition_type
            }
        )
        new_id_result = session.execute(text("SELECT @new_id")).fetchone()
        session.commit()
        return new_id_result[0] if new_id_result else None
    except Exception as e:
        print(f"❌ Erreur AddReactor : {e}")
        session.rollback()
        return None


def update_reactor(
    reactor_pk, reactor_name_id, reactor_id, image_url, reactor_tier_id,
    optimized_condition_type
):
    try:
        session.execute(
            text("""
                CALL UpdateReactor(
                    :p_id,
                    :p_reactor_name_id,
                    :p_reactor_id,
                    :p_image_url,
                    :p_reactor_tier_id,
                    :p_optimized_condition_type
                )
            """),
            {
                "p_id": reactor_pk,
                "p_reactor_name_id": reactor_name_id,
                "p_reactor_id": reactor_id,
                "p_image_url": image_url,
                "p_reactor_tier_id": reactor_tier_id,
                "p_optimized_condition_type": optimized_condition_type
            }
        )
        session.commit()
        return True
    except Exception as e:
        print(f"❌ Erreur UpdateReactor : {e}")
        session.rollback()
        return False


# ---------- table reactor_skill_power ----------
def get_reactor_skill_power(reactor_id, level):
    try:
        result = session.execute(
            text("CALL GetReactorSkillPower(:p_reactor_id, :p_level)"),
            {"p_reactor_id": reactor_id, "p_level": level}
        )
        row = result.fetchone()
        session.commit()
        return row[0] if row else None
    except Exception as e:
        print(f"❌ Erreur GetReactorSkillPower : {e}")
        session.rollback()
        return None


def add_reactor_skill_power(
    reactor_id, level, skill_atk_power, sub_skill_atk_power
):
    try:
        session.execute(
            text("""
                CALL AddReactorSkillPower(
                    :p_reactor_id,
                    :p_level,
                    :p_skill_atk_power,
                    :p_sub_skill_atk_power,
                    @new_id
                )
            """),
            {
                "p_reactor_id": reactor_id,
                "p_level": level,
                "p_skill_atk_power": skill_atk_power,
                "p_sub_skill_atk_power": sub_skill_atk_power
            }
        )
        new_id_result = session.execute(text("SELECT @new_id")).fetchone()
        session.commit()
        return new_id_result[0] if new_id_result else None
    except Exception as e:
        print(f"❌ Erreur AddReactorSkillPower : {e}")
        session.rollback()
        return None


def update_reactor_skill_power(
    pk, reactor_id, level, skill_atk_power, sub_skill_atk_power
):
    try:
        session.execute(
            text("""
                CALL UpdateReactorSkillPower(
                    :p_id,
                    :p_reactor_id,
                    :p_level,
                    :p_skill_atk_power,
                    :p_sub_skill_atk_power
                )
            """),
            {
                "p_id": pk,
                "p_reactor_id": reactor_id,
                "p_level": level,
                "p_skill_atk_power": skill_atk_power,
                "p_sub_skill_atk_power": sub_skill_atk_power
            }
        )
        session.commit()
        return True
    except Exception as e:
        print(f"❌ Erreur UpdateReactorSkillPower : {e}")
        session.rollback()
        return False


# ---------- table reactor_skill_power_coeff ----------
def get_reactor_coeff(reactor_id, level, coeff_stat_id):
    try:
        result = session.execute(
            text("CALL GetReactorCoeff(:p_reactor_id, :p_level, :p_coeff_stat_id)"),
            {
                "p_reactor_id": reactor_id,
                "p_level": level,
                "p_coeff_stat_id": coeff_stat_id
            }
        )
        row = result.fetchone()
        session.commit()
        return row[0] if row else None
    except Exception as e:
        print(f"❌ Erreur GetReactorCoeff : {e}")
        session.rollback()
        return None


def add_reactor_coeff(
    reactor_id, level, coeff_stat_id, coeff_stat_value
):
    try:
        session.execute(
            text("""
                CALL AddReactorCoeff(
                    :p_reactor_id,
                    :p_level,
                    :p_coeff_stat_id,
                    :p_coeff_stat_value,
                    @new_id
                )
            """),
            {
                "p_reactor_id": reactor_id,
                "p_level": level,
                "p_coeff_stat_id": coeff_stat_id,
                "p_coeff_stat_value": coeff_stat_value
            }
        )
        new_id_result = session.execute(text("SELECT @new_id")).fetchone()
        session.commit()
        return new_id_result[0] if new_id_result else None
    except Exception as e:
        print(f"❌ Erreur AddReactorCoeff : {e}")
        session.rollback()
        return None


def update_reactor_coeff(
    pk, reactor_id, level, coeff_stat_id, coeff_stat_value
):
    try:
        session.execute(
            text("""
                CALL UpdateReactorCoeff(
                    :p_id,
                    :p_reactor_id,
                    :p_level,
                    :p_coeff_stat_id,
                    :p_coeff_stat_value
                )
            """),
            {
                "p_id": pk,
                "p_reactor_id": reactor_id,
                "p_level": level,
                "p_coeff_stat_id": coeff_stat_id,
                "p_coeff_stat_value": coeff_stat_value
            }
        )
        session.commit()
        return True
    except Exception as e:
        print(f"❌ Erreur UpdateReactorCoeff : {e}")
        session.rollback()
        return False


# ---------- table reactor_enchant_effect ----------
def get_reactor_enchant(reactor_id, level, enchant_level, stat_id):
    try:
        result = session.execute(
            text(
                "CALL GetReactorEnchant(:p_reactor_id, :p_level, :p_enchant_level, :p_stat_id)"
            ),
            {
                "p_reactor_id": reactor_id,
                "p_level": level,
                "p_enchant_level": enchant_level,
                "p_stat_id": stat_id
            }
        )
        row = result.fetchone()
        session.commit()
        return row[0] if row else None
    except Exception as e:
        print(f"❌ Erreur GetReactorEnchant : {e}")
        session.rollback()
        return None


def add_reactor_enchant(
    reactor_id, level, enchant_level, stat_id, value
):
    try:
        session.execute(
            text("""
                CALL AddReactorEnchant(
                    :p_reactor_id,
                    :p_level,
                    :p_enchant_level,
                    :p_stat_id,
                    :p_value,
                    @new_id
                )
            """),
            {
                "p_reactor_id": reactor_id,
                "p_level": level,
                "p_enchant_level": enchant_level,
                "p_stat_id": stat_id,
                "p_value": value
            }
        )
        new_id_result = session.execute(text("SELECT @new_id")).fetchone()
        session.commit()
        return new_id_result[0] if new_id_result else None
    except Exception as e:
        print(f"❌ Erreur AddReactorEnchant : {e}")
        session.rollback()
        return None


def update_reactor_enchant(
    pk, reactor_id, level, enchant_level, stat_id, value
):
    try:
        session.execute(
            text("""
                CALL UpdateReactorEnchant(
                    :p_id,
                    :p_reactor_id,
                    :p_level,
                    :p_enchant_level,
                    :p_stat_id,
                    :p_value
                )
            """),
            {
                "p_id": pk,
                "p_reactor_id": reactor_id,
                "p_level": level,
                "p_enchant_level": enchant_level,
                "p_stat_id": stat_id,
                "p_value": value
            }
        )
        session.commit()
        return True
    except Exception as e:
        print(f"❌ Erreur UpdateReactorEnchant : {e}")
        session.rollback()
        return False
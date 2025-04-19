from sql.database import SessionLocal
from sqlalchemy import text

session = SessionLocal()

# ============================================
# CRUD – Descendant
# ============================================

def get_descendant(descendant_id: int):
    try:
        res = session.execute(
            text("CALL GetDescendant(:p_descendant_id)"),
            {"p_descendant_id": descendant_id}
        )
        row = res.fetchone()
        session.commit()
        return row
    except Exception as e:
        print(f"❌ get_descendant : {e}")
        session.rollback()
        return None


def add_descendant(descendant_id: int, name_id: int,
                   group_id: int, image_url: str):
    try:
        session.execute(
            text("""
                CALL AddDescendant(
                    :p_descendant_id,
                    :p_descendant_name,
                    :p_descendant_group_id,
                    :p_descendant_image_url,
                    @new_id
                )
            """),
            {
                "p_descendant_id": descendant_id,
                "p_descendant_name": name_id,
                "p_descendant_group_id": group_id,
                "p_descendant_image_url": image_url
            }
        )
        new_id = session.execute(text("SELECT @new_id")).fetchone()[0]
        session.commit()
        return new_id
    except Exception as e:
        print(f"❌ add_descendant : {e}")
        session.rollback()
        return None


def update_descendant(record_id: int, descendant_id: int, name_id: int,
                      group_id: int, image_url: str):
    try:
        session.execute(
            text("""
                CALL UpdateDescendant(
                    :p_id,
                    :p_descendant_id,
                    :p_descendant_name,
                    :p_descendant_group_id,
                    :p_descendant_image_url
                )
            """),
            {
                "p_id": record_id,
                "p_descendant_id": descendant_id,
                "p_descendant_name": name_id,
                "p_descendant_group_id": group_id,
                "p_descendant_image_url": image_url
            }
        )
        session.commit()
        return True
    except Exception as e:
        print(f"❌ update_descendant : {e}")
        session.rollback()
        return False


# ============================================
# CRUD – Descendant Stat
# ============================================

def get_descendant_stat(descendant_id: int, level: int):
    try:
        res = session.execute(
            text("CALL GetDescendantStat(:p_descendant_id, :p_level)"),
            {"p_descendant_id": descendant_id, "p_level": level}
        )
        row = res.fetchone()
        session.commit()
        return row
    except Exception as e:
        print(f"❌ get_descendant_stat : {e}")
        session.rollback()
        return None


def add_descendant_stat(descendant_id: int, level: int):
    try:
        session.execute(
            text("CALL AddDescendantStat(:p_descendant_id, :p_level, @new_id)"),
            {"p_descendant_id": descendant_id, "p_level": level}
        )
        new_id = session.execute(text("SELECT @new_id")).fetchone()[0]
        session.commit()
        return new_id
    except Exception as e:
        print(f"❌ add_descendant_stat : {e}")
        session.rollback()
        return None


def update_descendant_stat(record_id: int, descendant_id: int, level: int):
    try:
        session.execute(
            text("""
                CALL UpdateDescendantStat(:p_id, :p_descendant_id, :p_level)
            """),
            {"p_id": record_id, "p_descendant_id": descendant_id, "p_level": level}
        )
        session.commit()
        return True
    except Exception as e:
        print(f"❌ update_descendant_stat : {e}")
        session.rollback()
        return False


# ============================================
# CRUD – Descendant Stat Detail
# ============================================

def get_descendant_stat_detail(descendant_id: int, level: int, stat_id: int):
    try:
        res = session.execute(
            text("""
                CALL GetDescendantStatDetail(
                    :p_descendant_id, :p_level, :p_stat_id)
            """),
            {
                "p_descendant_id": descendant_id,
                "p_level": level,
                "p_stat_id": stat_id
            }
        )
        row = res.fetchone()
        session.commit()
        return row
    except Exception as e:
        print(f"❌ get_descendant_stat_detail : {e}")
        session.rollback()
        return None


def add_descendant_stat_detail(descendant_id: int, level: int,
                               stat_id: int, stat_value: float):
    try:
        session.execute(
            text("""
                CALL AddDescendantStatDetail(
                    :p_descendant_id, :p_level,
                    :p_stat_id, :p_stat_value, @new_id)
            """),
            {
                "p_descendant_id": descendant_id,
                "p_level": level,
                "p_stat_id": stat_id,
                "p_stat_value": stat_value
            }
        )
        new_id = session.execute(text("SELECT @new_id")).fetchone()[0]
        session.commit()
        return new_id
    except Exception as e:
        print(f"❌ add_descendant_stat_detail : {e}")
        session.rollback()
        return None


def update_descendant_stat_detail(record_id: int, descendant_id: int, level: int,
                                  stat_id: int, stat_value: float):
    try:
        session.execute(
            text("""
                CALL UpdateDescendantStatDetail(
                    :p_id, :p_descendant_id, :p_level,
                    :p_stat_id, :p_stat_value)
            """),
            {
                "p_id": record_id,
                "p_descendant_id": descendant_id,
                "p_level": level,
                "p_stat_id": stat_id,
                "p_stat_value": stat_value
            }
        )
        session.commit()
        return True
    except Exception as e:
        print(f"❌ update_descendant_stat_detail : {e}")
        session.rollback()
        return False


# ============================================
# CRUD – Descendant Skill
# ============================================

def get_descendant_skill(descendant_id: int, skill_name_id: int):
    try:
        res = session.execute(
            text("""
                CALL GetDescendantSkill(:p_descendant_id, :p_skill_name)
            """),
            {"p_descendant_id": descendant_id, "p_skill_name": skill_name_id}
        )
        row = res.fetchone()
        session.commit()
        return row
    except Exception as e:
        print(f"❌ get_descendant_skill : {e}")
        session.rollback()
        return None


def add_descendant_skill(descendant_id: int, skill_type_id: int, skill_name_id: int,
                         element_type_id: int, arche_type_id: int,
                         image_url: str, skill_desc_id: int):
    try:
        session.execute(
            text("""
                CALL AddDescendantSkill(
                    :p_descendant_id, :p_skill_type, :p_skill_name,
                    :p_element_type, :p_arche_type,
                    :p_skill_image_url, :p_skill_description, @new_id)
            """),
            {
                "p_descendant_id": descendant_id,
                "p_skill_type": skill_type_id,
                "p_skill_name": skill_name_id,
                "p_element_type": element_type_id,
                "p_arche_type": arche_type_id,
                "p_skill_image_url": image_url,
                "p_skill_description": skill_desc_id
            }
        )
        new_id = session.execute(text("SELECT @new_id")).fetchone()[0]
        session.commit()
        return new_id
    except Exception as e:
        print(f"❌ add_descendant_skill : {e}")
        session.rollback()
        return None


def update_descendant_skill(record_id: int, descendant_id: int, skill_type_id: int,
                            skill_name_id: int, element_type_id: int, arche_type_id: int,
                            image_url: str, skill_desc_id: int):
    try:
        session.execute(
            text("""
                CALL UpdateDescendantSkill(
                    :p_id, :p_descendant_id, :p_skill_type, :p_skill_name,
                    :p_element_type, :p_arche_type,
                    :p_skill_image_url, :p_skill_description)
            """),
            {
                "p_id": record_id,
                "p_descendant_id": descendant_id,
                "p_skill_type": skill_type_id,
                "p_skill_name": skill_name_id,
                "p_element_type": element_type_id,
                "p_arche_type": arche_type_id,
                "p_skill_image_url": image_url,
                "p_skill_description": skill_desc_id
            }
        )
        session.commit()
        return True
    except Exception as e:
        print(f"❌ update_descendant_skill : {e}")
        session.rollback()
        return False
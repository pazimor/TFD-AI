from sql.database import SessionLocal
from sqlalchemy import text

session = SessionLocal()

# ==============================
# CRUD for core_slot
# ==============================

def get_core_slot(core_slot_db_id):
    try:
        result = session.execute(
            text("CALL GetCoreSlot(:p_id)"),
            {"p_id": core_slot_db_id}
        )
        row = result.fetchone()
        session.commit()
        return row if row else None
    except Exception as e:
        print(f"❌ Erreur dans get_core_slot : {e}")
        session.rollback()
        return None

def add_core_slot(core_slot_id, available_weapon, available_core_type):
    try:
        session.execute(
            text("""
                CALL AddCoreSlot(
                    :p_core_slot_id,
                    :p_available_weapon,
                    :p_available_core_type,
                    @new_id
                )
            """),
            {
                "p_core_slot_id": core_slot_id,
                "p_available_weapon": available_weapon,
                "p_available_core_type": available_core_type
            }
        )
        new_id_result = session.execute(text("SELECT @new_id")).fetchone()
        session.commit()
        return new_id_result[0] if new_id_result else None
    except Exception as e:
        print(f"❌ Erreur dans add_core_slot : {e}")
        session.rollback()
        return None

def update_core_slot(core_slot_db_id, core_slot_id, available_weapon, available_core_type):
    try:
        session.execute(
            text("""
                CALL UpdateCoreSlot(
                    :p_id,
                    :p_core_slot_id,
                    :p_available_weapon,
                    :p_available_core_type
                )
            """),
            {
                "p_id": core_slot_db_id,
                "p_core_slot_id": core_slot_id,
                "p_available_weapon": available_weapon,
                "p_available_core_type": available_core_type
            }
        )
        session.commit()
        return True
    except Exception as e:
        print(f"❌ Erreur dans update_core_slot : {e}")
        session.rollback()
        return False

# ==============================
# CRUD for core_type
# ==============================

def get_core_type(core_type_db_id):
    try:
        result = session.execute(
            text("CALL GetCoreType(:p_id)"),
            {"p_id": core_type_db_id}
        )
        row = result.fetchone()
        session.commit()
        return row if row else None
    except Exception as e:
        print(f"❌ Erreur dans get_core_type : {e}")
        session.rollback()
        return None

def add_core_type(core_type_id_value, core_type_value):
    try:
        session.execute(
            text("""
                CALL AddCoreType(
                    :p_core_type_id,
                    :p_core_type,
                    @new_id
                )
            """),
            {
                "p_core_type_id": core_type_id_value,
                "p_core_type": core_type_value
            }
        )
        new_id_result = session.execute(text("SELECT @new_id")).fetchone()
        session.commit()
        return new_id_result[0] if new_id_result else None
    except Exception as e:
        print(f"❌ Erreur dans add_core_type : {e}")
        session.rollback()
        return None

def update_core_type(core_type_db_id, core_type_id_value, core_type_value):
    try:
        session.execute(
            text("""
                CALL UpdateCoreType(
                    :p_id,
                    :p_core_type_id,
                    :p_core_type
                )
            """),
            {
                "p_id": core_type_db_id,
                "p_core_type_id": core_type_id_value,
                "p_core_type": core_type_value
            }
        )
        session.commit()
        return True
    except Exception as e:
        print(f"❌ Erreur dans update_core_type : {e}")
        session.rollback()
        return False

# ==============================
# CRUD for core_option
# ==============================

def get_core_option(core_type_id: int, core_option_id: int):
    try:
        result = session.execute(
            text("CALL GetCoreOption(:p_core_type_id, :p_core_option_id)"),
            {"p_core_type_id": core_type_id, "p_core_option_id": core_option_id}
        )
        row = result.fetchone()
        session.commit()
        return row
    except Exception as e:
        print(f"❌ Erreur dans get_core_option : {e}")
        session.rollback()
        return None

def add_core_option(core_type_id: int, core_option_id: int):
    try:
        session.execute(
            text("CALL AddCoreOption(:p_core_type_id, :p_core_option_id, @new_id)"),
            {"p_core_type_id": core_type_id, "p_core_option_id": core_option_id}
        )
        new_id = session.execute(text("SELECT @new_id")).fetchone()[0]
        session.commit()
        return new_id
    except Exception as e:
        print(f"❌ Erreur dans add_core_option : {e}")
        session.rollback()
        return None

def update_core_option(record_id: int, core_type_id: int, core_option_id: int):
    try:
        session.execute(
            text("CALL UpdateCoreOption(:p_id, :p_core_type_id, :p_core_option_id)"),
            {"p_id": record_id, "p_core_type_id": core_type_id, "p_core_option_id": core_option_id}
        )
        session.commit()
        return True
    except Exception as e:
        print(f"❌ Erreur dans update_core_option : {e}")
        session.rollback()
        return False

# ==============================
# CRUD for core_option_detail
# ==============================

def get_core_option_detail(required_meta_id: int):
    try:
        result = session.execute(
            text("CALL GetCoreOptionDetail(:p_required_meta_id)"),
            {"p_required_meta_id": required_meta_id}
        )
        row = result.fetchone()
        session.commit()
        return row
    except Exception as e:
        print(f"❌ Erreur dans get_core_option_detail : {e}")
        session.rollback()
        return None

def add_core_option_detail(core_option_id: int, core_option_grade: int, required_meta_type: str, required_meta_id: int, required_count: int):
    try:
        session.execute(
            text("""
                CALL AddCoreOptionDetail(
                    :p_core_option_id,
                    :p_core_option_grade,
                    :p_required_meta_type,
                    :p_required_meta_id,
                    :p_required_count,
                    @new_id
                )
            """),
            {
                "p_core_option_id": core_option_id,
                "p_core_option_grade": core_option_grade,
                "p_required_meta_type": required_meta_type,
                "p_required_meta_id": required_meta_id,
                "p_required_count": required_count
            }
        )
        new_id = session.execute(text("SELECT @new_id")).fetchone()[0]
        session.commit()
        return new_id
    except Exception as e:
        print(f"❌ Erreur dans add_core_option_detail : {e}")
        session.rollback()
        return None

def update_core_option_detail(record_id: int, core_option_id: int, core_option_grade: int, required_meta_type: str, required_meta_id: int, required_count: int):
    try:
        session.execute(
            text("""
                CALL UpdateCoreOptionDetail(
                    :p_id,
                    :p_core_option_id,
                    :p_core_option_grade,
                    :p_required_meta_type,
                    :p_required_meta_id,
                    :p_required_count
                )
            """),
            {
                "p_id": record_id,
                "p_core_option_id": core_option_id,
                "p_core_option_grade": core_option_grade,
                "p_required_meta_type": required_meta_type,
                "p_required_meta_id": required_meta_id,
                "p_required_count": required_count
            }
        )
        session.commit()
        return True
    except Exception as e:
        print(f"❌ Erreur dans update_core_option_detail : {e}")
        session.rollback()
        return False

# ==============================
# CRUD for core_available_item_option
# ==============================

def get_core_available_item_option(core_option_id: int, option_grade: int, stat_id: int):
    try:
        result = session.execute(
            text("""
                CALL GetCoreAvailableItemOption(
                    :p_core_option_id,
                    :p_option_grade,
                    :p_stat_id
                )
            """),
            {"p_core_option_id": core_option_id, "p_option_grade": option_grade, "p_stat_id": stat_id}
        )
        row = result.fetchone()
        session.commit()
        return row
    except Exception as e:
        print(f"❌ Erreur dans get_core_available_item_option : {e}")
        session.rollback()
        return None


def add_core_available_item_option(core_option_id: int, item_option: int, option_type: int, option_grade: int,
                                     stat_id: int, operator_type: int, min_stat_value: int, max_stat_value: int, rate: int):
    try:
        session.execute(
            text("""
                CALL AddCoreAvailableItemOption(
                    :p_core_option_id,
                    :p_item_option,
                    :p_option_type,
                    :p_option_grade,
                    :p_stat_id,
                    :p_operator_type,
                    :p_min_stat_value,
                    :p_max_stat_value,
                    :p_rate,
                    @new_id
                )
            """),
            {
                "p_core_option_id": core_option_id,
                "p_item_option": item_option,
                "p_option_type": option_type,
                "p_option_grade": option_grade,
                "p_stat_id": stat_id,
                "p_operator_type": operator_type,
                "p_min_stat_value": min_stat_value,
                "p_max_stat_value": max_stat_value,
                "p_rate": rate
            }
        )
        new_id = session.execute(text("SELECT @new_id")).fetchone()[0]
        session.commit()
        return new_id
    except Exception as e:
        print(f"❌ Erreur dans add_core_available_item_option : {e}")
        session.rollback()
        return None

def update_core_available_item_option(record_id: int, core_option_id: int, item_option: int, option_type: int, option_grade: int,
                                        stat_id: int, operator_type: int, min_stat_value: int, max_stat_value: int, rate: int):
    try:
        session.execute(
            text("""
                CALL UpdateCoreAvailableItemOption(
                    :p_id,
                    :p_core_option_id,
                    :p_item_option,
                    :p_option_type,
                    :p_option_grade,
                    :p_stat_id,
                    :p_operator_type,
                    :p_min_stat_value,
                    :p_max_stat_value,
                    :p_rate
                )
            """),
            {
                "p_id": record_id,
                "p_core_option_id": core_option_id,
                "p_item_option": item_option,
                "p_option_type": option_type,
                "p_option_grade": option_grade,
                "p_stat_id": stat_id,
                "p_operator_type": operator_type,
                "p_min_stat_value": min_stat_value,
                "p_max_stat_value": max_stat_value,
                "p_rate": rate
            }
        )
        session.commit()
        return True
    except Exception as e:
        print(f"❌ Erreur dans update_core_available_item_option : {e}")
        session.rollback()
        return False
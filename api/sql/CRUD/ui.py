import json

from sql.database import SessionLocal
from sqlalchemy import text

session = SessionLocal()

# ---------- Get all modules (+ stats) -------------------------------
def get_all_modules():
    try:
        result = session.execute(text("CALL GetAllModules()")).mappings().all()
        session.commit()
        return [dict(r) for r in result]
    except Exception as e:
        print(f"❌ GetAllModules : {e}")
        session.rollback()
        return []


def get_all_translations():
    try:
        rows = session.execute(text("CALL GetAllTranslations()")).mappings().all()
        session.commit()
        return [dict(r) for r in rows]
    except Exception as e:
        session.rollback()
        print(f"❌ GetAllTranslations : {e}")
        return []

def get_all_descendants():
    try:
        rows = session.execute(text("CALL GetAllDescendants()")).mappings().all()
        session.commit()
        data = [dict(r) for r in rows]

        return data
    except Exception as e:
        print(f"❌ get_all_descendants_full : {e}")
        session.rollback()
        return []

def get_all_weapons_full():
    try:
        rows = session.execute(text("CALL GetAllWeapons()")).mappings().all()
        session.commit()
        data = [dict(r) for r in rows]
        for w in data:
            for k in ("stats", "skills"):
                raw = w.get(k)
                if isinstance(raw, str):
                    try:
                        w[k] = json.loads(raw)
                    except json.JSONDecodeError:
                        pass
        return data
    except Exception as e:
        print(f"❌ get_all_weapons_full : {e}")
        session.rollback()
        return []

def get_weapon_core_slots(weapon_id: int):
    try:
        row = session.execute(
            text("CALL GetWeaponCoreSlots(:wid)"),
            {"wid": weapon_id}
        ).mappings().first()
        session.commit()
        import json
        if row:
            result = dict(row)
            # slot_options arrive en texte JSON → list[dict]
            if isinstance(result["slot_options"], str):
                try:
                    result["slot_options"] = json.loads(result["slot_options"])
                except json.JSONDecodeError:
                    result["slot_options"] = []
            return result
        return {}
    except Exception as e:
        print(f"❌ get_weapon_core_slots : {e}")
        session.rollback()
        return {}

def get_all_external_components_full():
    try:
        rows = session.execute(
            text("CALL GetAllExternalComponents()")
        ).mappings().all()
        session.commit()
        data = [dict(r) for r in rows]

        for comp in data:
            for key in ("base_stat", "set_option_detail"):
                raw = comp.get(key)
                if isinstance(raw, str):
                    try:
                        comp[key] = json.loads(raw)
                    except json.JSONDecodeError:
                        comp[key] = []
        return data
    except Exception as e:
        print(f"❌ get_all_external_components_full : {e}")
        session.rollback()
        return []

def get_all_reactors_full():
    try:
        rows = session.execute(
            text("CALL GetAllReactors()")
        ).mappings().all()
        session.commit()

        data = [dict(r) for r in rows]
        for rec in data:
            for key in ("base_stat", "set_option_detail", "skill_power"):
                raw = rec.get(key)
                if isinstance(raw, str):
                    try:
                        rec[key] = json.loads(raw)
                    except json.JSONDecodeError:
                        rec[key] = []
        return data
    except Exception as e:
        print(f"❌ get_all_reactors_full : {e}")
        session.rollback()
        return []

def get_all_boards_full():
    try:
        rows = session.execute(text("CALL GetAllBoards()")).mappings().all()
        session.commit()

        data = [dict(r) for r in rows]
        for b in data:
            raw_nodes = b.get("nodes")
            if isinstance(raw_nodes, str):
                try:
                    b["nodes"] = json.loads(raw_nodes)
                except json.JSONDecodeError:
                    b["nodes"] = []
        return data
    except Exception as e:
        print(f"❌ get_all_boards_full : {e}")
        session.rollback()
        return []
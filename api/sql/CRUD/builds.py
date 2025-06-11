from sqlalchemy import text
import json
from sql.database import SessionLocal
from sqlalchemy.orm import Session
from sql.model import UserBuild


def add_build(user_id: str, name: str, data: dict) -> UserBuild | None:
    session: Session = SessionLocal()
    try:
        result = session.execute(
            text("CALL AddUserBuild(:user_id, :build_name, :build_data)"),
            {"user_id": user_id, "build_name": name, "build_data": json.dumps(data)}
        )
        new_id = result.scalar()
        session.commit()
        return get_build(new_id)
    except Exception as e:
        print(f"❌ add_build (SP): {e}")
        session.rollback()
        return None
    finally:
        session.close()

def get_user_builds(user_id: str):
    session: Session = SessionLocal()
    try:
        rows = session.execute(
            text("CALL GetUserBuilds(:user_id)"),
            {"user_id": user_id}
        ).fetchall()
        return [row for row in rows]
    except Exception as e:
        print(f"❌ get_user_builds (SP): {e}")
        return []
    finally:
        session.close()


def get_build(build_id: int) -> UserBuild | None:
    session: Session = SessionLocal()
    try:
        row = session.execute(
            text("CALL GetUserBuild(:build_id)"),
            {"build_id": build_id}
        ).first()
        return row
    except Exception as e:
        print(f"❌ get_build (SP): {e}")
        return None
    finally:
        session.close()


def update_build(build_id: int, user_id: str, name: str, data: dict) -> bool:
    session: Session = SessionLocal()
    try:
        result = session.execute(
            text("CALL UpdateUserBuild(:build_id, :user_id, :build_name, :build_data)"),
            {"build_id": build_id, "user_id": user_id, "build_name": name, "build_data": json.dumps(data)}
        )
        session.commit()
        return result.rowcount > 0
    except Exception as e:
        print(f"❌ update_build (SP): {e}")
        session.rollback()
        return False
    finally:
        session.close()

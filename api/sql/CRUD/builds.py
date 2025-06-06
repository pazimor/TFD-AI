from sql.database import SessionLocal
from sqlalchemy.orm import Session
from sql.model import UserBuild


def add_build(user_id: str, name: str, data: dict) -> UserBuild | None:
    session: Session = SessionLocal()
    try:
        build = UserBuild(user_id=user_id, build_name=name, build_data=data)
        session.add(build)
        session.commit()
        session.refresh(build)
        return build
    except Exception as e:
        print(f"\u274c add_build : {e}")
        session.rollback()
        return None
    finally:
        session.close()


def get_user_builds(user_id: str):
    session: Session = SessionLocal()
    try:
        return session.query(UserBuild).filter_by(user_id=user_id).all()
    except Exception as e:
        print(f"\u274c get_user_builds : {e}")
        return []
    finally:
        session.close()


def get_build(build_id: int) -> UserBuild | None:
    session: Session = SessionLocal()
    try:
        return session.query(UserBuild).filter_by(build_id=build_id).first()
    except Exception as e:
        print(f"\u274c get_build : {e}")
        return None
    finally:
        session.close()


def update_build(build_id: int, user_id: str, name: str, data: dict) -> bool:
    session: Session = SessionLocal()
    try:
        build = session.query(UserBuild).filter_by(build_id=build_id, user_id=user_id).first()
        if not build:
            return False
        build.build_name = name
        build.build_data = data
        session.commit()
        return True
    except Exception as e:
        print(f"\u274c update_build : {e}")
        session.rollback()
        return False
    finally:
        session.close()

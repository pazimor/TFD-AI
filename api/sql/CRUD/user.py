from sql.database import SessionLocal
from sqlalchemy import text
import requests

session = SessionLocal()

def sync_user(user):
    try:
        photo_bytes = b''
        if user.get("photoUrl"):
            try:
                resp = requests.get(user["photoUrl"], timeout=5)
                if resp.ok:
                    photo_bytes = resp.content
            except Exception:
                photo_bytes = b''
        session.execute(
            text("CALL SyncUser(:p_user_id, :p_user_name, :p_user_email, :p_photo)"),
            {
                "p_user_id": user['id'],
                "p_user_name": user["name"],
                "p_user_email": user["email"],
                "p_photo": photo_bytes,
            }
        )
        session.commit()
        return None
    except Exception as e:
        print(f"❌ Erreur : {e}")
        session.rollback()
        return None

def fetch_settings(user_id):
    try:
        result = session.execute(
            text("CALL GetUserSettings(:p_user_id)"),
            {
                "p_user_id": user_id
            }
        )
        row = result.fetchone()
        session.commit()
        return row[1] if row else None
    except Exception as e:
        print(f"❌ Erreur : {e}")
        session.rollback()
        return None

def set_user_settings(user_id, default_language):
    try:
        session.execute(
            text("CALL SetUserSettings(:p_user_id, :p_default_language)"),
            {
                "p_user_id": user_id,
                "p_default_language": default_language
            }
        )
        session.commit()
        return True
    except Exception as e:
        print(f"❌ Erreur : {e}")
        session.rollback()
        return False

def get_photo(user_id):
    try:
        result = session.execute(
            text("CALL GetUserPhoto(:p_user_id)"),
            {"p_user_id": user_id}
        )
        row = result.fetchone()
        session.commit()
        return row[0] if row else None
    except Exception as e:
        print(f"❌ Erreur : {e}")
        session.rollback()
        return None

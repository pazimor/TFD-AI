from sql.database import SessionLocal
from sqlalchemy import text

session = SessionLocal()

# ================================
# CRUD for translation_strings
# ================================
def test():
    result = session.execute(text("""SELECT COUNT(*) FROM translation_strings;"""))
    if result.returns_rows:
        rows = result.fetchall()
        print(rows)

def add_translation(**data):
    try:
        query = text("""
            CALL AddTranslation(
                :p_fr, :p_ko, :p_en, :p_de, :p_ja, :p_zh_cn, :p_zh_tw,
                :p_it, :p_pl, :p_pt, :p_ru, :p_es
            )
        """)
        result = session.execute(query, {
            "p_fr": data.get("fr"),
            "p_ko": data.get("ko"),
            "p_en": data.get("en"),
            "p_de": data.get("de"),
            "p_ja": data.get("ja"),
            "p_zh_cn": data.get("zh_cn"),
            "p_zh_tw": data.get("zh_tw"),
            "p_it": data.get("it"),
            "p_pl": data.get("pl"),
            "p_pt": data.get("pt"),
            "p_ru": data.get("ru"),
            "p_es": data.get("es")
        })
        inserted_id = result.fetchone()[0]
        session.commit()
        return inserted_id
    except Exception as e:
        print(f"❌ Erreur : {e}")
        session.rollback()
        return None
    finally:
        pass


def update_translation(language_id, **data):
    try:
        query = text("""
            CALL UpdateTranslation(
                :p_id, :p_fr, :p_ko, :p_en, :p_de, :p_ja, :p_zh_cn, :p_zh_tw,
                :p_it, :p_pl, :p_pt, :p_ru, :p_es
            )
        """)
        session.execute(query, {
            "p_id": language_id,
            "p_fr": data.get("fr"),
            "p_ko": data.get("ko"),
            "p_en": data.get("en"),
            "p_de": data.get("de"),
            "p_ja": data.get("ja"),
            "p_zh_cn": data.get("zh_cn"),
            "p_zh_tw": data.get("zh_tw"),
            "p_it": data.get("it"),
            "p_pl": data.get("pl"),
            "p_pt": data.get("pt"),
            "p_ru": data.get("ru"),
            "p_es": data.get("es")
        })
        session.commit()
        return True
    except Exception as e:
        print(f"❌ Erreur : {e}")
        session.rollback()
        return None
    finally:
        pass

def upsert_translation(language_id, **data):
    try:
        result = session.execute(text("""
            CALL UpsertTranslation(
                :p_id, :p_fr, :p_ko, :p_en, :p_de, :p_ja, :p_zh_cn, :p_zh_tw,
                :p_it, :p_pl, :p_pt, :p_ru, :p_es
            );
        """), {
            "p_id": language_id,
            "p_fr": data.get("fr"),
            "p_ko": data.get("ko"),
            "p_en": data.get("en"),
            "p_de": data.get("de"),
            "p_ja": data.get("ja"),
            "p_zh_cn": data.get("zh_cn"),
            "p_zh_tw": data.get("zh_tw"),
            "p_it": data.get("it"),
            "p_pl": data.get("pl"),
            "p_pt": data.get("pt"),
            "p_ru": data.get("ru"),
            "p_es": data.get("es")
        })

        # Vérifier si le résultat renvoie des lignes
        if result.returns_rows:
            rows = result.fetchall()
            return rows[0][0]
        else:
            # Si aucune ligne n'est retournée, considérer que c'est une mise à jour et renvoyer l'id fourni
            return language_id if language_id != 0 else None
    except Exception as e:
        print(f"❌ Erreur : {e}")
        session.rollback()
        return None

def get_item(language_id):
    try:
        result = session.execute(text("CALL GetTranslation(:p_language_id)"), { "p_language_id": language_id })
        language = result.fetchall()
        return language
    except Exception as e:
        print(f"❌ Erreur : {e}")
        session.rollback()
    finally:
        pass

def find_translation(language_column, search_text):
    try:
        result = session.execute(
            text("CALL FindTranslation(:p_language_column, :p_search_text)"),
            {
                "p_language_column": language_column,
                "p_search_text": search_text
            }
        )
        row = result.fetchone()
        return row[0] if row else 0
    except Exception as e:
        print(f"❌ Erreur : {e}")
        session.rollback()
    finally:
        pass

# ================================
# functions for translation_strings
# ================================

def parse_for_languages(lang, translation, language_id=0):
    """
    Si language_id est fourni (non nul), met à jour le record existant correspondant.
    Sinon, insère un nouveau record avec la traduction pour la langue donnée et retourne le nouvel id.
    """
    # Dictionnaire de base avec toutes les langues initialisées à une chaîne vide
    translation_data = {
        'fr': '',
        'ko': '',
        'en': '',
        'de': '',
        'ja': '',
        'zh_cn': '',
        'zh_tw': '',
        'it': '',
        'pl': '',
        'pt': '',
        'ru': '',
        'es': '',
    }

    if language_id == 0:
        # Aucun record existant : insérer un nouveau record
        if lang in translation_data:
            translation_data[lang] = translation
        else:
            translation_data['fr'] = translation
        new_id = add_translation(**translation_data)
        print("Insert: ", new_id, translation_data)
        return new_id
    else:
        # Id fourni, tenter de récupérer le record existant
        current = get_item(language_id)
        if current and len(current) > 0:
            current_dict = dict(current[0]._mapping)
            current_dict[lang] = translation
            update_translation(current_dict['id'], **current_dict)
            print("Update: ", current_dict)
            return current_dict['id']
        else:
            # L'id fourni n'existe pas, insérer un nouveau record
            if lang in translation_data:
                translation_data[lang] = translation
            else:
                translation_data['fr'] = translation
            new_id = upsert_translation(0, **translation_data)
            print("Insert: ", new_id, translation_data)
            return new_id
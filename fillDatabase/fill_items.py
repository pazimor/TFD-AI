import json
import requests
import api.sql.crud as crud
from api.sql import SessionLocal
from sqlalchemy import text

# Langues supportées
languages = ["fr", "ko", "en", "de", "ja", "zh-CN", "zh-TW", "it", "pl", "pt", "ru", "es"]

# URL de base (ne dépend plus d'une langue)
BASE_URL = "https://open.api.nexon.com/static/tfd/meta"
WEAPONS_URL = "weapon.json"
DESCENDANTS_URL = "descendant.json"
STATISTICS_URL = "stat.json"

def fetch_url(url):
    """Récupère les données depuis l'URL spécifiée."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur lors de la récupération : {e}")
        return []

def fetch_all(target_url):
    """Récupère les données pour tous les langages pour l'URL cible."""
    all_data = {}
    for lang in languages:
        url = f"{BASE_URL}/{lang}/{target_url}"
        data = fetch_url(url)
        if data is not None:
            all_data[lang] = data
    return all_data

def parse_weapon(lang, weapon, stat):
    """
    Parse une arme pour correspondre aux paramètres de la procédure stockée.
    On construit des champs multi-langues pour 'name' et 'capabilities'.
    """
    weapon_type = weapon["weapon_type"]
    munitions = weapon["weapon_rounds_type"]
    ability_name = weapon["weapon_perk_ability_name"]
    ability_description = weapon["weapon_perk_ability_description"]

    # Stockage multi-langue du nom
    name = { lang: weapon["weapon_name"] }

    # Stockage multi-langue de la capacité, si présente
    if ability_name:
        capabilities = { lang: f"{ability_name}: {ability_description}" }
    else:
        capabilities = None

    statistics = {
        stat.get(item["stat_id"], item["stat_id"]): str(item["stat_value"])
        for item in weapon["base_stat"]
    }
    displaydata = {
        "img": weapon["image_url"],
        "tier": weapon["weapon_tier_id"]
    }

    parsed = {
        "id": int(weapon["weapon_id"]),
        "name": name,
        "type": f"weapon, {weapon_type}, {munitions}",
        "goals": None,
        "capabilities": capabilities,
        "statistics": statistics,
        "displaydata": displaydata
    }
    return parsed

def parse_descendants(lang, descendant, stat):
    """
    Parse un descendant pour correspondre aux paramètres de la procédure stockée.
    On construit des champs multi-langues pour 'name' et 'capabilities'.
    """
    capabilities_str = " ".join(
        f"{item['skill_type']}, {item['skill_name']}, {item['element_type']}, {item['arche_type']}: {item['skill_description']}"
        for item in descendant["descendant_skill"]
    )
    capabilities = { lang: capabilities_str } if capabilities_str else None
    name = { lang: descendant["descendant_name"] }
    # On suppose que descendant_stat[39] existe (à adapter si besoin)
    statistics = {
        stat.get(item["stat_id"], item["stat_id"]): str(item["stat_value"])
        for item in descendant["descendant_stat"][39]["stat_detail"]
    }
    displaydata = { "img": descendant["descendant_image_url"] }

    parsed = {
        "id": int(descendant["descendant_id"]),
        "name": name,
        "type": "descendant",
        "goals": None,
        "capabilities": capabilities,
        "statistics": statistics,
        "displaydata": displaydata
    }
    return parsed

def add_items(session, item):
    """
    Ajoute ou met à jour un item en base de données via les procédures stockées.
    Les champs 'name' et 'capabilities' sont sérialisés en JSON.
    """
    try:
        existing = session.execute(
            text("CALL GetItem(:id)"),
            {"id": item["id"]}
        ).fetchone()

        name_json = json.dumps(item["name"], ensure_ascii=False)
        capabilities_json = json.dumps(item["capabilities"], ensure_ascii=False) if item["capabilities"] is not None else None
        statistics_json = json.dumps(item["statistics"], ensure_ascii=False)
        display_json = json.dumps(item["displaydata"], ensure_ascii=False)

        if not existing:
            crud.add_item(item["id"], name_json, item["type"], item["goals"], capabilities_json, statistics_json, display_json)
        else:
            crud.update_item(item["id"], name_json, item["type"], item["goals"], capabilities_json, statistics_json, display_json)
    except Exception as e:
        print(f"❌ Erreur lors de l'ajout/mise à jour de l'item '{item['name']}': {e}")
        session.rollback()

def main():
    """Fonction principale pour remplir la table des items avec multi-langue."""
    session = SessionLocal()
    try:
        # Récupération des statistiques (on utilise le français pour la conversion)
        stats = fetch_url(f"{BASE_URL}/fr/{STATISTICS_URL}")
        stats_dict = { s["stat_id"]: s["stat_name"] for s in stats }

        # Récupération multi-langue des armes
        weapons_by_lang = fetch_all(WEAPONS_URL)
        all_weapons = {}
        for lang, weapons in weapons_by_lang.items():
            for weapon in weapons:
                weapon_id = int(weapon["weapon_id"])
                parsed_weapon = parse_weapon(lang, weapon, stats_dict)
                if weapon_id in all_weapons:
                    # Fusionner les données multi-langues
                    all_weapons[weapon_id]["name"].update(parsed_weapon["name"])
                    if parsed_weapon["capabilities"]:
                        if all_weapons[weapon_id]["capabilities"] is None:
                            all_weapons[weapon_id]["capabilities"] = parsed_weapon["capabilities"]
                        else:
                            all_weapons[weapon_id]["capabilities"].update(parsed_weapon["capabilities"])
                else:
                    all_weapons[weapon_id] = parsed_weapon

        for weapon in all_weapons.values():
            add_items(session, weapon)

        # Récupération multi-langue des descendants
        descendants_by_lang = fetch_all(DESCENDANTS_URL)
        all_descendants = {}
        for lang, descendants in descendants_by_lang.items():
            for descendant in descendants:
                descendant_id = int(descendant["descendant_id"])
                parsed_desc = parse_descendants(lang, descendant, stats_dict)
                if descendant_id in all_descendants:
                    all_descendants[descendant_id]["name"].update(parsed_desc["name"])
                    if parsed_desc["capabilities"]:
                        if all_descendants[descendant_id]["capabilities"] is None:
                            all_descendants[descendant_id]["capabilities"] = parsed_desc["capabilities"]
                        else:
                            all_descendants[descendant_id]["capabilities"].update(parsed_desc["capabilities"])
                else:
                    all_descendants[descendant_id] = parsed_desc

        for descendant in all_descendants.values():
            add_items(session, descendant)

    finally:
        session.close()

if __name__ == "__main__":
    main()
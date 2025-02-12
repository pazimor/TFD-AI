import json
import requests
import sql.crud as crud
from sql.database import (SessionLocal)
from sqlalchemy import text

# URL de l'API Nexon pour les modules
lang = "fr"

BASE_URL = f"https://open.api.nexon.com/static/tfd/meta/{lang}"
DESCENDANTS_URL = f"{BASE_URL}/descendant.json"
WEAPONS_URL = f"{BASE_URL}/weapon.json"
STATISTICS_URL = f"{BASE_URL}/stat.json"

def fetch_url(url):
    """Récupère les modules depuis l'URL spécifiée."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        modules = response.json()
        return modules
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur lors de la récupération : {e}")
        return []

def parse_weapon(weapon, stat):
    """Parse une arme pour correspondre aux paramètres de la procédure stockée."""

    type = weapon["weapon_type"]
    munitions = weapon["weapon_rounds_type"]
    ability_name = weapon["weapon_perk_ability_name"]
    ability_description = weapon["weapon_perk_ability_description"]

    capability = None
    if ability_name is not None:
        capability = f"{ability_name}: {ability_description}"

    statistics = {stat.get(item['stat_id'], item['stat_id']): str(item['stat_value']) for item in weapon["base_stat"]}

    displaydata = {"img": weapon["image_url"], "tier": weapon["weapon_tier_id"]}

    parsed = {
        "id": weapon["weapon_id"],
        "name": weapon["weapon_name"],
        "type": f"weapon, {type}, {munitions}",
        "goals": None,
        "capabilities": capability,
        "statistics": statistics,
        "displaydata": displaydata
    }
    return parsed

def parse_descendants(descendant, stat):
    """Parse un descendant pour correspondre aux paramètres de la procédure stockée."""

    capabilities = " ".join(
        f" {item['skill_type']}, {item['skill_name']}, {item['element_type']}, {item['arche_type']}: {item['skill_description']}"
        for i, item in enumerate(descendant["descendant_skill"])
    )
    statistics = {
        stat.get(item["stat_id"], item["stat_id"]): str(item["stat_value"])
        for item in descendant["descendant_stat"][39]["stat_detail"]
    }

    displaydata = {"img": descendant["descendant_image_url"]}

    parsed = {
        "id": descendant["descendant_id"],
        "name": descendant["descendant_name"],
        "type": "descendant",
        "goals": None,
        "capabilities": capabilities,
        "statistics": statistics,
        "displaydata": displaydata
    }
    return parsed

def add_items(session, item):
    """Ajoute ou met à jour un item en base de données en utilisant les procédures stockées."""

    try:
        existing = session.execute(
            text("CALL GetItem(:id)"),
            {"id": item["id"]}
        ).fetchone()

        statistics_json = json.dumps(item["statistics"], ensure_ascii=False)
        display_json = json.dumps(item["displaydata"], ensure_ascii=False)

        if not existing:
            crud.add_item(item["id"], item["name"], item["type"], item["goals"], item["capabilities"], statistics_json, display_json)
        else:
            crud.update_item(item["id"], item["name"], item["type"], item["goals"], item["capabilities"], statistics_json, display_json)
    except Exception as e:
        print(f"❌ Erreur lors de l'ajout/mise à jour du modifier '{item['name']}': {e}")
        session.rollback()

def main():
    """Fonction principale pour remplir la table des modifiers."""

    session = SessionLocal()
    try:
        """ Statistics """
        stats = fetch_url(STATISTICS_URL)
        stats_dict = {stat["stat_id"]: stat["stat_name"] for stat in stats}

        """ Weapons """
        weapons = fetch_url(WEAPONS_URL)
        for weapon in weapons:
            parsed_weapon = parse_weapon(weapon, stats_dict)
            add_items(session, parsed_weapon)

        """ Descendants """
        reactors = fetch_url(DESCENDANTS_URL)
        for reactor in reactors:
            parsed_reactor = parse_descendants(reactor, stats_dict)
            add_items(session, parsed_reactor)
    finally:
        session.close()

if __name__ == "__main__":
    main()
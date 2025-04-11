import re
import requests

from time import sleep
from sql.CRUD import items
from sqlalchemy import text
from request_service import fetch_url, fetch_multy_lang, languages_bdd
from sql.CRUD import translation_strings
from sql.CRUD.translation_strings import parse_for_languages

BASE_URL = "https://open.api.nexon.com/static/tfd/meta"

WEAPONS_URL = "weapon.json"
DESCENDANTS_URL = "descendant.json"
STATISTICS_URL = "stat.json"

#TODO: implementer les statistiques optionels (aleatoire)
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
        ## add perk img
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

def get_fixed_lang(lang):
    """Return the fixed language code: use the original if French, else reformat."""
    return lang if lang == "fr" else re.sub(r'_([a-z]{2})', lambda m: '-' + m.group(1).upper(), lang)

def fill_items():
    """Fonction principale pour remplir la table des items avec multi-langue."""
    sleep(0.1)
    try:
        print(f"Fetch data from API endpoints\r", end='', flush=True)
        stats = fetch_multy_lang(STATISTICS_URL)
        all_weapons = fetch_multy_lang(WEAPONS_URL)
        all_descendants = fetch_multy_lang(DESCENDANTS_URL)

        indexed_stats = {}
        indexed_weapons = {}
        indexed_descendants = {}
        for lang in languages_bdd:
            fixed_lang = get_fixed_lang(lang)
            indexed_stats[fixed_lang] = { stat["stat_id"]: stat for stat in stats[fixed_lang] }
            indexed_weapons[fixed_lang] = { weapon["weapon_id"]: weapon for weapon in all_weapons[fixed_lang] }
            indexed_descendants[fixed_lang] = { descendant["descendant_id"]: descendant for descendant in all_descendants[fixed_lang] }

        print(f"Inject Statistics            \r", end='', flush=True)
        stats_dict = {}
        for stat_id, stat_fr in indexed_stats["fr"].items():
            id_in_DB = parse_for_languages("fr", stat_fr["stat_name"])
            stats_dict[stat_id] = id_in_DB
            for lang in languages_bdd:
                if lang == "fr":
                    continue
                fixed_lang = get_fixed_lang(lang)
                if stat_id in indexed_stats[fixed_lang]:
                    parse_for_languages(lang, indexed_stats[fixed_lang][stat_id]["stat_name"], id_in_DB)

        print(f"Inject Weapons   \r", end='', flush=True)
        for weapon in all_weapons["fr"]:
            id_name = parse_for_languages("fr", weapon["weapon_name"])
            id_perk = parse_for_languages("fr", f"{weapon['weapon_perk_ability_name']}: {weapon['weapon_perk_ability_description']}")

            parsed_weapon = parse_weapon("fr", weapon, stats_dict)
            parsed_weapon["name"] = id_name
            parsed_weapon["capabilities"] = id_perk

            for lang in languages_bdd:
                if lang == "fr":
                    continue
                fixed_lang = get_fixed_lang(lang)
                if weapon["weapon_id"] in indexed_weapons[fixed_lang]:
                    weapon_lang = indexed_weapons[fixed_lang][weapon["weapon_id"]]
                    parse_for_languages(lang, weapon_lang["weapon_name"], id_name)
                    parse_for_languages(lang,f"{weapon_lang['weapon_perk_ability_name']}: {weapon_lang['weapon_perk_ability_description']}", id_perk)
            items.add_items(parsed_weapon)

        print(f"Inject Descendants\r", end='', flush=True)
        for descendant in all_descendants["fr"]:
            id_name = parse_for_languages("fr", descendant["descendant_name"])
            capabilities_ids = []
            for item in descendant["descendant_skill"]:
                cap_str = f"{item['skill_type']}, {item['skill_name']}, {item['element_type']}, {item['arche_type']}: {item['skill_description']}"
                cap_id = parse_for_languages("fr", cap_str)
                capabilities_ids.append(cap_id)

            parsed_descendant = parse_descendants("fr", descendant, stats_dict)
            parsed_descendant["name"] = id_name
            parsed_descendant["capabilities"] = capabilities_ids

            for lang in languages_bdd:
                if lang == "fr":
                    continue
                fixed_lang = get_fixed_lang(lang)
                if descendant["descendant_id"] in indexed_descendants[fixed_lang]:
                    descendant_lang = indexed_descendants[fixed_lang][descendant["descendant_id"]]
                    parse_for_languages(lang, descendant_lang["descendant_name"], id_name)
                    for i, item in enumerate(descendant_lang["descendant_skill"]):
                        cap_str_lang = f"{item['skill_type']}, {item['skill_name']}, {item['element_type']}, {item['arche_type']}: {item['skill_description']}"
                        parse_for_languages(lang, cap_str_lang, capabilities_ids[i])
            items.add_items(parsed_descendant)
    finally:
        print("finished          ")
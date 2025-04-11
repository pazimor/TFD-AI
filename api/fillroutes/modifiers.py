import re
import json
import requests

from time import sleep
from sqlalchemy import text
from sql.CRUD import modifiers
from parsing import parse_effect_line
from sql.CRUD import translation_strings
from sql.CRUD.translation_strings import parse_for_languages
from request_service import fetch_url, fetch_multy_lang, languages, languages_bdd, get_fixed_lang

BASE_URL = f"https://open.api.nexon.com/static/tfd/meta"
EXTERNAL_COMPONENT_URL = "external-component.json"
REACTORS_URL = f"reactor.json"
STATISTICS_URL = f"stat.json"
MODULES_URL = "module.json"

def parse_module(lang, module):
    """Parse un module pour correspondre aux paramètres de la procédure stockée."""

    type = module["module_type"] or "None"
    clas = module["module_class"] or "None"
    weatype = module["available_weapon_type"] or "None"
    if type == "None":
        type = module["available_module_slot_type"] or "None"
        if type != "None":
            type = type[0]
            if type == "Main":
                type = "None"

    totale = f"Module, {type}, {clas}"
    if weatype != "None":
        totale = f"Module, {type}, {clas}, {weatype[0]}"

    displaydata = { "img": module["image_url"], "tier": module["module_tier_id"] }

    name = { lang: module["module_name"] }


    parsed = {
        "id": int(module["module_id"]),
        "name": name,
        "type": totale,
        "statistics": "",
        "stack_id": "1" if type != "None" else "10",
        "stack_description": None,
        "displaydata": displaydata
    }
    return parsed

#TODO: implementer les statistiques optionels (aleatoire)
def parse_external(lang, externalComponant, stats_dict):
    """Parse un composant externe pour correspondre aux paramètres de la procédure stockée."""

    base_stat = externalComponant["base_stat"][99]
    statId = base_stat["stat_id"]
    statValue = base_stat["stat_value"]

    description = None
    if len(externalComponant["set_option_detail"]) >= 1:
        description = " ".join(
            f"{item['set_option']}, stack: {item['set_count']}, effect: {item['set_option_effect']}"
            for i, item in enumerate(externalComponant["set_option_detail"])
        )

    displaydata = {"img": externalComponant["image_url"], "tier": externalComponant["external_component_tier_id"]}

    statistics = {stats_dict[statId]: f"+{statValue}"}

    name = { lang: externalComponant["external_component_name"] }
    parsed = {
        "id": int(externalComponant["external_component_id"]),
        "name": name,
        "type": f"ExternalComponant, {externalComponant['external_component_equipment_type']}, Légataire",
        "statistics": statistics,
        "stack_id": "4",
        "stack_description": description,
        "displaydata": displaydata
    }
    return parsed

#TODO: implementer les statistiques optionels (aleatoire)
def parse_reactor(lang, reactor, stat):
    """Parse un composant externe pour correspondre aux paramètres de la procédure stockée."""

    if (reactor["reactor_name"] == None):
        return None

    statistics = {}
    if len(reactor["reactor_skill_power"]) >= 99:
        reactor_stat = reactor["reactor_skill_power"][99]
        statistics = {
            stat[item['coefficient_stat_id']]: f"+{item['coefficient_stat_value']}%"
            for i, item in enumerate(reactor_stat["skill_power_coefficient"])
        }

    weapon = reactor["optimized_condition_type"]
    if isinstance(weapon, tuple) and len(weapon) == 1:
        weapon = weapon[0]

    displaydata = {"img": reactor["image_url"], "tier": reactor["reactor_tier_id"]}

    name = {lang: reactor["reactor_name"]}


    parsed = {
        "id": int(reactor["reactor_id"]),
        "name": name,
        "type": f"reactor, {weapon}, Légataire",
        "statistics": statistics,
        "stack_id": "1",
        "stack_description": None,
        "displaydata": displaydata
    }
    return parsed

def fill_modifiers():
    """Fonction principale pour remplir la table des modifiers."""
    sleep(0.1)
    try:
        print("Fetch data from API endpoints\r", end='', flush=True)
        stats = fetch_multy_lang(STATISTICS_URL)
        all_modules = fetch_multy_lang(MODULES_URL)
        all_externals = fetch_multy_lang(EXTERNAL_COMPONENT_URL)
        all_reactors = fetch_multy_lang(REACTORS_URL)

        # Pre-index data for stats, modules, externals, and reactors by their respective IDs
        indexed_stats = {}
        indexed_modules = {}
        indexed_externals = {}
        indexed_reactors = {}
        for lang in languages_bdd:
            fixed_lang = get_fixed_lang(lang)
            indexed_stats[fixed_lang] = { stat["stat_id"]: stat for stat in stats[fixed_lang] }
            indexed_modules[fixed_lang] = { module["module_id"]: module for module in all_modules[fixed_lang] }
            indexed_externals[fixed_lang] = { external["external_component_id"]: external for external in all_externals[fixed_lang] }
            indexed_reactors[fixed_lang] = { reactor["reactor_id"]: reactor for reactor in all_reactors[fixed_lang] }

        print("Inject Statistics            \r", end='', flush=True)
        stats_dict = {}
        for stat_id, stat_fr in indexed_stats["fr"].items():
            id_in_DB = parse_for_languages("fr", stat_fr["stat_name"])
            stats_dict[stat_id] = id_in_DB

        perk_dict = {}
        print("Inject Modules    \r", end='', flush=True)
        for module in all_modules["fr"]:
            id_name = parse_for_languages("fr", module["module_name"])
            perk = parse_effect_line(module["module_stat"][-1]["value"], perk_dict)
            current_perk = {}
            for item in perk:
                id_perk = translation_strings.find_translation('fr', item)
                if id_perk == 0:
                    id_perk = parse_for_languages("fr", item)
                current_perk = {id_perk: perk[item]}
                perk_dict[id_perk] = item

            parsed_module = parse_module("fr", module)

            parsed_module["name"] = id_name
            parsed_module["statistics"] = current_perk
            for lang in languages_bdd:
                if lang == "fr":
                    continue
                fixed_lang = get_fixed_lang(lang)
                if module["module_id"] in indexed_modules[fixed_lang]:
                    module_lang = indexed_modules[fixed_lang][module["module_id"]]
                    parse_for_languages(lang, module_lang["module_name"], id_name)
                    parse_for_languages(lang, module["module_stat"][-1]["value"], id_perk)
            modifiers.add_modifiers(parsed_module)

        print("Inject External Components\r", end='', flush=True)
        for external in all_externals["fr"]:
            id_name = parse_for_languages("fr", external["external_component_name"])
            parsed_external = parse_external("fr", external, stats_dict)
            parsed_external["name"] = id_name
            for lang in languages_bdd:
                if lang == "fr":
                    continue
                fixed_lang = get_fixed_lang(lang)
                if external["external_component_id"] in indexed_externals[fixed_lang]:
                    external_lang = indexed_externals[fixed_lang][external["external_component_id"]]
                    parse_for_languages(lang, external_lang["external_component_name"], id_name)
            modifiers.add_modifiers(parsed_external)

        print("Inject Reactor            \r", end='', flush=True)
        for reactor in all_reactors["fr"]:
            id_name = parse_for_languages("fr", reactor["reactor_name"])
            parsed_reactor = parse_reactor("fr", reactor, stats_dict)
            if parsed_reactor == None:
                continue
            parsed_reactor["name"] = id_name
            for lang in languages_bdd:
                if lang == "fr":
                    continue
                fixed_lang = get_fixed_lang(lang)
                if reactor["reactor_id"] in indexed_reactors[fixed_lang]:
                    reactor_lang = indexed_reactors[fixed_lang][reactor["reactor_id"]]
                    parse_for_languages(lang, reactor_lang["reactor_name"], id_name)
            modifiers.add_modifiers(parsed_reactor)

    finally:
        print("finished          ")
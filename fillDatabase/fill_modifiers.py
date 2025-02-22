import json
import requests
import sql.crud as crud
from sql.database import (SessionLocal)
from sqlalchemy import text

# URL de l'API Nexon pour les modules
languages = ["fr", "ko", "en", "de", "ja", "zh-CN", "zh-TW", "it", "pl", "pt", "ru", "es"]

BASE_URL = f"https://open.api.nexon.com/static/tfd/meta"
EXTERNAL_COMPONENT_URL = "external-component.json"
REACTORS_URL = f"{BASE_URL}/fr/reactor.json"
STATISTICS_URL = f"{BASE_URL}/fr/stat.json"
MODULES_URL = "module.json"

def fetch_urls(url):
    """Récupère les modules depuis l'URL spécifiée."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        modules = response.json()
        return modules
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur lors de la récupération : {e}")
        return []

def fetch_all(target_url):
    all_modules = {}
    for lang in languages:
        url = f"{BASE_URL}/{lang}/{target_url}"
        modules = fetch_urls(url)
        if modules is not None:
            all_modules[lang] = modules
    return all_modules

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
        "statistics": module["module_stat"][-1]["value"],
        "stack_id": "1" if type != "None" else "10",
        "stack_description": None,
        "displaydata": displaydata
    }
    return parsed

#TODO: implementer les statistiques optionels (aleatoire)
def parse_external(lang, externalComponant, stat):
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

    name = { lang: externalComponant["external_component_name"] }
    parsed = {
        "id": int(externalComponant["external_component_id"]),
        "name": name,
        "type": f"ExternalComponant, {externalComponant['external_component_equipment_type']}, Légataire",
        "statistics": f"{stat[statId]} +{statValue}",
        "stack_id": "4",
        "stack_description": description,
        "displaydata": displaydata
    }
    return parsed

#TODO: implementer les statistiques optionels (aleatoire)
def parse_reactor(reactor, stat):
    """Parse un composant externe pour correspondre aux paramètres de la procédure stockée."""

    statistics = ""
    if len(reactor["reactor_skill_power"]) >= 99:
        reactor_stat = reactor["reactor_skill_power"][99]

        statistics = " ".join(
            f"{stat[item['coefficient_stat_id']]} +{item['coefficient_stat_value']}%"
            for i, item in enumerate(reactor_stat["skill_power_coefficient"])
        )

    weapon = reactor["optimized_condition_type"]
    if isinstance(weapon, tuple) and len(weapon) == 1:
        weapon = weapon[0]

    displaydata = {"img": reactor["image_url"], "tier": reactor["reactor_tier_id"]}

    name = {"fr": reactor["reactor_name"]}

    parsed = {
        "id": int(reactor["reactor_id"]),
        "name": name,
        "type": f"reactor, {weapon}, Légataire",
        "statistics": f"{statistics}",
        "stack_id": "1",
        "stack_description": None,
        "displaydata": displaydata
    }
    return parsed

def add_modifier(session, modifier):
    """Ajoute ou met à jour un modifier en base de données en utilisant les procédures stockées."""
    try:
        existing = session.execute(
            text("CALL GetModifier(:id)"),
            {"id": modifier["id"]}
        ).fetchone()

        display_json = json.dumps(modifier["displaydata"], ensure_ascii=False)
        name = json.dumps(modifier["name"], ensure_ascii=False)

        if not existing:
            crud.add_modifier(modifier["id"], name, modifier["type"], modifier["statistics"], modifier["stack_id"], modifier["stack_description"], display_json)
        else:
            crud.update_modifier(modifier["id"], name, modifier["type"], modifier["statistics"], modifier["stack_id"], modifier["stack_description"], display_json)
    except Exception as e:
        print(f"❌ Erreur lors de l'ajout/mise à jour du modifier '{modifier['name']}': {e}")
        session.rollback()

def main():
    """Fonction principale pour remplir la table des modifiers."""

    session = SessionLocal()
    try:
        """ Statistics """
        stats = fetch_urls(STATISTICS_URL)
        stats_dict = {stat["stat_id"]: stat["stat_name"] for stat in stats}

        '''
        """ Modules """
        modules_by_lang = fetch_all(MODULE_URL)
        all_modules = {}

        for lang, modules in modules_by_lang.items():
            for module in modules:
                module_id = int(module["module_id"])
                parsed_module = parse_module(lang, module)
                if module_id in all_modules:
                    all_modules[module_id]["name"] = {**all_modules[module_id]["name"], **parsed_module["name"]}
                else:
                    all_modules[module_id] = parsed_module

        for module in all_modules.values():
            add_modifier(session, module)
        '''

        """ External Components """
        externals_by_lang = fetch_all(EXTERNAL_COMPONENT_URL)
        all_externals = {}

        for lang, externals in externals_by_lang.items():
            for external in externals:
                parsed_external = parse_external(lang, external, stats_dict)
                external_id = int(parsed_external["id"])
                if external_id in all_externals:
                    all_externals[external_id]["name"] = {**all_externals[external_id]["name"], **parsed_external["name"]}
                else:
                    all_externals[external_id] = parsed_external

        for external in all_externals.values():
            add_modifier(session, external)

        """ Reactor """
        reactors = fetch_urls(REACTORS_URL)
        for reactor in reactors:
            parsed_reactor = parse_reactor(reactor, stats_dict)
            if (parsed_reactor["name"]["fr"] is not None):
                add_modifier(session, parsed_reactor)
    finally:
        session.close()

if __name__ == "__main__":
    main()
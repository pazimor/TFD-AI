from request_service import fetch_multy_lang, languages_bdd, get_fixed_lang
from sql.CRUD.translation_strings import parse_for_languages
from sql.CRUD import weapon as crud_weapon
from sql.CRUD import weapon_base_stat as crud_weapon_base_stat

WEAPONS_URL = "weapon.json"

def fetch_weapons(stats_dict):
    """used to fill weapons"""
    try:
        all_weapons = fetch_multy_lang(WEAPONS_URL)

        for lang in languages_bdd:
            fixed_lang = get_fixed_lang(lang)
            parse_for_languages(fixed_lang, None, 1)

        indexed_weapons = {}
        for lang in languages_bdd:
            fixed_lang = get_fixed_lang(lang)
            indexed_weapons[fixed_lang] = {weapon["weapon_id"]: weapon for weapon in all_weapons[fixed_lang]}

        for weapon in all_weapons["fr"]:
            id_name = None
            id_type = None
            id_round_type = None
            id_perk = None
            id_perk_description = None

            for lang in languages_bdd:
                fixed_lang = get_fixed_lang(lang)
                if lang == "fr":
                    id_name = parse_for_languages(lang, weapon["weapon_name"])
                    id_type = parse_for_languages(lang, weapon["weapon_type"])
                    id_round_type = parse_for_languages(lang, weapon["weapon_rounds_type"])
                    id_perk = parse_for_languages(lang, weapon['weapon_perk_ability_name'])
                    id_perk_description = parse_for_languages(lang, weapon["weapon_perk_ability_description"])
                    continue
                if weapon["weapon_id"] in indexed_weapons[fixed_lang]:
                    weapon_lang = indexed_weapons[fixed_lang][weapon["weapon_id"]]
                    parse_for_languages(lang, weapon_lang["weapon_name"], id_name)
                    parse_for_languages(lang, weapon_lang["weapon_type"], id_type)
                    parse_for_languages(lang, weapon_lang["weapon_rounds_type"], id_round_type)
                    parse_for_languages(lang, weapon_lang['weapon_perk_ability_name'], id_perk)
                    parse_for_languages(lang, weapon_lang["weapon_perk_ability_description"], id_perk_description)

            item = crud_weapon.get_weapon(weapon["weapon_id"])
            core_slot = weapon.get("available_core_slot")
            available_core_slot = ",".join(weapon["available_core_slot"]) if core_slot else "0"
            atk_type = stats_dict[weapon["firearm_atk"][99]["firearm"][0]["firearm_atk_type"]]
            if item is None:
                crud_weapon.add_weapon(id_name, weapon["weapon_id"],
                    weapon["image_url"], id_type,
                    weapon["weapon_tier_id"], id_round_type,
                    available_core_slot, id_perk,
                    id_perk_description, weapon["weapon_perk_ability_image_url"],
                    atk_type,
                    weapon["firearm_atk"][99]["firearm"][0]["firearm_atk_value"])
            else:
                crud_weapon.update_weapon(item, id_name, weapon["weapon_id"],
                    weapon["image_url"], id_type,
                    weapon["weapon_tier_id"], id_round_type,
                    available_core_slot, id_perk,
                    id_perk_description, weapon["weapon_perk_ability_image_url"],
                    atk_type,
                    weapon["firearm_atk"][99]["firearm"][0]["firearm_atk_value"])

            base_stats = weapon.get("base_stat", [])
            for base in base_stats:
                item = crud_weapon_base_stat.get_weapon_base_stat(
                    weapon["weapon_id"],
                    stats_dict[base["stat_id"]],
                )
                if item is None:
                    crud_weapon_base_stat.add_weapon_base_stat(
                        weapon["weapon_id"],
                        stats_dict[base["stat_id"]],
                        base["stat_value"])
                else:
                    crud_weapon_base_stat.update_weapon_base_stat(
                        item,
                        weapon["weapon_id"],
                        stats_dict[base["stat_id"]],
                        base["stat_value"])
    finally:
        pass
# cores.py
from request_service import fetch_multy_lang, fetch_url, languages_bdd, get_fixed_lang
from sql.CRUD import cors as crud_core
from sql.CRUD.translation_strings import parse_for_languages

BASE_URL = "https://open.api.nexon.com/static/tfd/meta"
CORES_TYPE_URL = "core-type.json"
CORES_SLOT_URL = "core-slot.json"


def fetch_cores(stats_dict):
    try:

        all_core_types = fetch_multy_lang(CORES_TYPE_URL)

        indexed_core_type = {}
        for lang in languages_bdd:
            fixed_lang = get_fixed_lang(lang)
            indexed_core_type[fixed_lang] = {type["core_type_id"]: type for type in all_core_types[fixed_lang]}

        for core in all_core_types["fr"]:
            id_core_type = None
            for lang in languages_bdd:
                fixed_lang = get_fixed_lang(lang)
                if lang == "fr":
                    id_core_type = parse_for_languages(fixed_lang, core["core_type"])
                    continue
                else:
                    core_type = indexed_core_type[fixed_lang][core["core_type_id"]]["core_type"]
                    parse_for_languages(fixed_lang, core_type, id_core_type)

            core_item = crud_core.get_core_type(core["core_type_id"])
            if core_item is None:
                crud_core.add_core_type(core["core_type_id"], id_core_type)
            else:
                crud_core.update_core_type(core_item.id, core["core_type_id"], id_core_type)

            for option in core["core_option"]:
                options_item = crud_core.get_core_option(core["core_type_id"], option["core_option_id"])
                if options_item is None:
                    crud_core.add_core_option(core["core_type_id"], option["core_option_id"])
                else:
                    crud_core.update_core_option(core_item.id, core["core_type_id"], option["core_option_id"])

                for detail in option["detail"]:
                    detail_item = crud_core.get_core_option_detail(detail["required_core_item"]["meta_id"])
                    if detail_item is None:
                        crud_core.add_core_option_detail(
                            option["core_option_id"],
                            detail["core_option_grade"],
                            detail["required_core_item"]["meta_type"],
                            detail["required_core_item"]["meta_id"],
                            detail["required_core_item"]["count"])
                    else:
                        crud_core.update_core_option_detail(
                            detail_item.id,
                            option["core_option_id"],
                            detail["core_option_grade"],
                            detail["required_core_item"]["meta_type"],
                            detail["required_core_item"]["meta_id"],
                            detail["required_core_item"]["count"])

                    for stat in detail["available_item_option"]:
                        stat_item = crud_core.get_core_available_item_option(option["core_option_id"], stat["option_grade"], stat["option_effect"]["stat_id"])

                        if stat_item is None:
                            crud_core.add_core_available_item_option(
                                core["core_type_id"],
                                option["core_option_id"],
                                stat["option_type"],
                                stat["option_grade"],
                                stats_dict[stat["option_effect"]["stat_id"]],
                                stat["option_effect"]["operator_type"],
                                stat["option_effect"]["min_stat_value"],
                                stat["option_effect"]["max_stat_value"],
                                stat["rate"]
                            )
                        else:
                            crud_core.update_core_available_item_option(
                                stat_item.id,
                                core["core_type_id"],
                                option["core_option_id"],
                                stat["option_type"],
                                stat["option_grade"],
                                stats_dict[stat["option_effect"]["stat_id"]],
                                stat["option_effect"]["operator_type"],
                                stat["option_effect"]["min_stat_value"],
                                stat["option_effect"]["max_stat_value"],
                                stat["rate"]
                            )



    finally:
        # Vous pouvez ajouter ici la fermeture des ressources ou du logging final si besoin.
        pass

def fetch_slots():
    try:
        all_core_slots = fetch_url(f"{BASE_URL}/{CORES_SLOT_URL}")

        for slot in all_core_slots:
            for type in slot["available_core_type_id"]:
                slot_item = crud_core.get_core_slot(slot["core_slot_id"])
                if slot_item is None:
                    crud_core.add_core_slot(slot["core_slot_id"], slot["available_weapon_id"][0], type)
                else:
                    crud_core.update_core_slot(slot_item.id, slot["core_slot_id"], slot["available_weapon_id"][0], type)
    finally:
        pass
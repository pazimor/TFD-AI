# descendants.py
from request_service import (
    fetch_multy_lang, fetch_url,
    languages_bdd, get_fixed_lang
)
from sql.CRUD import descendants as crud_descendant      # nouveau module CRUD
from sql.CRUD.translation_strings import parse_for_languages

BASE_URL = "https://open.api.nexon.com/static/tfd/meta"
DESCENDANT_URL = "descendant.json"


def fetch_descendants(stats_dict):
    """
    Récupère les descendants dans toutes les langues, met‑à‑jour la BDD.
    `stats_dict` : mapping stat_id → translation_strings.id (déjà créé ailleurs).
    """
    try:
        all_descendants = fetch_multy_lang(DESCENDANT_URL)

        # indexation par langue & id
        indexed_desc = {}
        for lang in languages_bdd:
            fixed_lang = get_fixed_lang(lang)
            indexed_desc[fixed_lang] = {
                d["descendant_id"]: d for d in all_descendants[fixed_lang]
            }

        # On parcourt la langue de référence (FR dans le projet)
        for desc in all_descendants["fr"]:
            # === Nom du descendant (multi‑langues)
            name_id = None
            for lang in languages_bdd:
                fixed_lang = get_fixed_lang(lang)
                if lang == "fr":
                    name_id = parse_for_languages(fixed_lang, desc["descendant_name"])
                else:
                    other_name = indexed_desc[fixed_lang][desc["descendant_id"]]["descendant_name"]
                    parse_for_languages(fixed_lang, other_name, name_id)

            # === Descendant (insert / update)
            db_desc = crud_descendant.get_descendant(desc["descendant_id"])
            if db_desc is None:
                crud_descendant.add_descendant(
                    desc["descendant_id"], name_id,
                    desc["descendant_group_id"], desc["descendant_image_url"]
                )
            else:
                crud_descendant.update_descendant(
                    db_desc.id, desc["descendant_id"], name_id,
                    desc["descendant_group_id"], desc["descendant_image_url"]
                )

            # === Stats par niveau
            for stat in desc["descendant_stat"]:
                level = stat["level"]
                db_stat = crud_descendant.get_descendant_stat(desc["descendant_id"], level)
                if db_stat is None:
                    crud_descendant.add_descendant_stat(desc["descendant_id"], level)
                else:
                    crud_descendant.update_descendant_stat(db_stat.id, desc["descendant_id"], level)

                for sd in stat["stat_detail"]:
                    stat_id = stats_dict[sd["stat_id"]]
                    stat_value = sd["stat_value"]
                    db_detail = crud_descendant.get_descendant_stat_detail(
                        desc["descendant_id"], level, stat_id)
                    if db_detail is None:
                        crud_descendant.add_descendant_stat_detail(
                            desc["descendant_id"], level, stat_id, stat_value)
                    else:
                        crud_descendant.update_descendant_stat_detail(
                            db_detail.id, desc["descendant_id"], level, stat_id, stat_value)

            # === Compétences
            for skill in desc["descendant_skill"]:
                # skill_name & description → chaines traduisibles
                skill_name_id = None
                skill_type_id = None
                element_type_id = None
                arche_type_id = None
                for lang in languages_bdd:
                    fixed_lang = get_fixed_lang(lang)
                    if lang == "fr":
                        skill_name_id = parse_for_languages(fixed_lang, skill["skill_name"])
                        skill_desc_id = parse_for_languages(fixed_lang, skill["skill_description"])
                        skill_type_id = parse_for_languages(fixed_lang, skill["skill_type"])
                        element_type_id = parse_for_languages(fixed_lang, skill["element_type"])
                        if skill["arche_type"]:
                            arche_type_id = parse_for_languages(fixed_lang, skill["arche_type"])
                    else:
                        other_desc = indexed_desc[fixed_lang].get(desc["descendant_id"])
                        other_skill = next(
                            (s for s in other_desc["descendant_skill"]
                             if s["skill_image_url"] == skill["skill_image_url"]),
                            None
                        )
                        if other_skill:
                            parse_for_languages(fixed_lang, other_skill["skill_name"], skill_name_id)
                            parse_for_languages(fixed_lang, other_skill["skill_description"], skill_desc_id)
                            parse_for_languages(fixed_lang, other_skill["skill_type"], skill_type_id)
                            parse_for_languages(fixed_lang, other_skill["element_type"], element_type_id)
                            if other_skill["arche_type"]:
                                parse_for_languages(fixed_lang, other_skill["arche_type"], arche_type_id)
                        else:
                            parse_for_languages(fixed_lang, skill["skill_name"], skill_name_id)
                            parse_for_languages(fixed_lang, skill["skill_description"], skill_desc_id)
                            parse_for_languages(fixed_lang, skill["skill_type"], skill_type_id)
                            parse_for_languages(fixed_lang, skill["element_type"], element_type_id)
                            if skill["arche_type"]:
                                parse_for_languages(fixed_lang, skill["arche_type"], arche_type_id)

                db_skill = crud_descendant.get_descendant_skill(
                    desc["descendant_id"], skill_name_id)
                if db_skill is None:
                    crud_descendant.add_descendant_skill(
                        desc["descendant_id"],
                        skill_type_id,
                        skill_name_id,
                        element_type_id,
                        arche_type_id,
                        skill["skill_image_url"],
                        skill_desc_id
                    )
                else:
                    crud_descendant.update_descendant_skill(
                        db_skill.id,
                        desc["descendant_id"],
                        skill_type_id,
                        skill_name_id,
                        element_type_id,
                        arche_type_id,
                        skill["skill_image_url"],
                        skill_desc_id
                    )
    finally:
        # libérez ressources / logging si besoin
        pass
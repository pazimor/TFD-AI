"""
Remplissage de la table external_component (+ base_stat & set_option)
à partir de /static/tfd/meta/<lang>/external-component.json
"""
import re

from request_service import fetch_multy_lang, languages_bdd, get_fixed_lang
from sql.CRUD.translation_strings import parse_for_languages
from sql.CRUD import external_components as crud_ext_comp

EXTERNAL_COMPONENT_URL = "external-component.json"


def fetch_external_components(stats_dict):
    """
    stats_dict :  mapping "stat_id" (string) → id dans translation_strings
    """
    try:
        # Récupération multilingue
        all_components = fetch_multy_lang(EXTERNAL_COMPONENT_URL)

        # Injection des chaînes de trad vides pour toutes les langues
        for lang in languages_bdd:
            parse_for_languages(get_fixed_lang(lang), None, 1)

        # Indexation par langue / external_component_id
        indexed = {}
        for lang in languages_bdd:
            f_lang = get_fixed_lang(lang)
            indexed[f_lang] = {
                comp["external_component_id"]: comp for comp in all_components[f_lang]
            }

        # Langue pivot = FR
        for comp in all_components["fr"]:
            # ─────────── 1/ Chaînes de traduction ───────────
            id_name = id_type = id_set_opt = id_set_eff = None

            # Pivot
            id_name = parse_for_languages("fr", comp["external_component_name"])
            id_type = parse_for_languages("fr", comp["external_component_equipment_type"])

            # Autres langues
            for lang in languages_bdd:
                if lang == "fr":
                    continue
                f_lang = get_fixed_lang(lang)
                if comp["external_component_id"] not in indexed[f_lang]:
                    continue
                c_lang = indexed[f_lang][comp["external_component_id"]]
                parse_for_languages(lang, c_lang["external_component_name"], id_name)
                parse_for_languages(lang, c_lang["external_component_equipment_type"], id_type)

            # ─────────── 2/ Upsert composant ───────────
            row_pk = crud_ext_comp.get_external_component(comp["external_component_id"])
            if row_pk is None:
                row_pk = crud_ext_comp.add_external_component(
                    id_name,
                    comp["external_component_id"],
                    comp["image_url"],
                    id_type,
                    comp["external_component_tier_id"]
                )
            else:
                crud_ext_comp.update_external_component(
                    row_pk,
                    id_name,
                    comp["external_component_id"],
                    comp["image_url"],
                    id_type,
                    comp["external_component_tier_id"]
                )

            # ─────────── 3/ Base‑stats (par niveau) ───────────
            for base in comp.get("base_stat", []):
                level = base["level"]
                stat_id = stats_dict[base["stat_id"]]
                pk = crud_ext_comp.get_external_component_base_stat(
                    comp["external_component_id"],
                    stat_id,
                    level
                )
                if pk is None:
                    crud_ext_comp.add_external_component_base_stat(
                        comp["external_component_id"],
                        level,
                        stat_id,
                        base["stat_value"]
                    )
                else:
                    crud_ext_comp.update_external_component_base_stat(
                        pk,
                        comp["external_component_id"],
                        level,
                        stat_id,
                        base["stat_value"]
                    )

            # ─────────── 4/ Set‑bonus ───────────
            for detail in comp.get("set_option_detail", []):
                # 4.1 chaînes pivot FR
                id_opt = parse_for_languages("fr", detail["set_option"])
                id_eff = parse_for_languages("fr", detail["set_option_effect"])

                # 4.2 autres langues
                for lang in languages_bdd:
                    if lang == "fr":
                        continue
                    for f_lang in indexed:
                        if comp["external_component_id"] not in indexed[f_lang]:
                            continue
                        d_langs = next(
                            (
                                d
                                for d in indexed[f_lang][comp["external_component_id"]]["set_option_detail"]
                                if d["set_count"] == detail["set_count"]
                            ),
                            None
                        )
                        if d_langs:
                            parse_for_languages(lang, d_langs["set_option"], id_opt)
                            parse_for_languages(lang, d_langs["set_option_effect"], id_eff)

                pk = crud_ext_comp.get_external_component_set_option(
                    comp["external_component_id"],
                    id_opt
                )
                if pk is None:
                    crud_ext_comp.add_external_component_set_option(
                        comp["external_component_id"],
                        id_opt,
                        detail["set_count"],
                        id_eff
                    )
                else:
                    crud_ext_comp.update_external_component_set_option(
                        pk,
                        comp["external_component_id"],
                        id_opt,
                        detail["set_count"],
                        id_eff
                    )
    finally:
        pass  # pour cohérence avec weapons.py
import re

from request_service import (
    fetch_multy_lang,
    languages_bdd,
    get_fixed_lang
)
from sql.CRUD.translation_strings import parse_for_languages
from sql.CRUD import reactors as crud_reactors

REACTORS_URL = "reactor.json"

def fetch_reactors(stats_dict):
    """
    Récupère les données reactors dans toutes les langues,
    remplit ou met à jour la base de données.
    """
    try:
        all_reactors = fetch_multy_lang(REACTORS_URL)

        # Pré‑indexation des traductions
        for lang in languages_bdd:
            fixed_lang = get_fixed_lang(lang)
            parse_for_languages(fixed_lang, None, 1)

        indexed_reactors = {}
        for lang in languages_bdd:
            fixed_lang = get_fixed_lang(lang)
            indexed_reactors[fixed_lang] = {
                reactor["reactor_id"]: reactor
                for reactor in all_reactors[fixed_lang]
            }

        # On se base sur la version FR comme pivot, comme pour les weapons
        for reactor in all_reactors["fr"]:
            # ------------------ traductions ------------------
            id_name = id_opt_cond = None

            for lang in languages_bdd:
                fixed_lang = get_fixed_lang(lang)
                if lang == "fr":
                    id_name = parse_for_languages(lang, reactor["reactor_name"])
                    id_opt_cond = parse_for_languages(lang, reactor["optimized_condition_type"])
                    continue
                if reactor["reactor_id"] in indexed_reactors[fixed_lang]:
                    reactor_lang = indexed_reactors[fixed_lang][reactor["reactor_id"]]
                    parse_for_languages(lang, reactor_lang["reactor_name"], id_name)
                    parse_for_languages(lang, reactor_lang["optimized_condition_type"], id_opt_cond)

            # ------------------ table principale reactor ------------------
            item = crud_reactors.get_reactor(reactor["reactor_id"])
            if item is None:
                crud_reactors.add_reactor(
                    id_name,
                    reactor["reactor_id"],
                    reactor["image_url"],
                    reactor["reactor_tier_id"],
                    id_opt_cond
                )
            else:
                crud_reactors.update_reactor(
                    item,
                    id_name,
                    reactor["reactor_id"],
                    reactor["image_url"],
                    reactor["reactor_tier_id"],
                    id_opt_cond
                )

            # ------------------ reactor_skill_power & enfants ------------------
            for sp in reactor.get("reactor_skill_power", []):
                lvl = sp["level"]
                sp_pk = crud_reactors.get_reactor_skill_power(reactor["reactor_id"], lvl)

                if sp_pk is None:
                    sp_pk = crud_reactors.add_reactor_skill_power(
                        reactor["reactor_id"],
                        lvl,
                        sp["skill_atk_power"],
                        sp["sub_skill_atk_power"]
                    )
                else:
                    crud_reactors.update_reactor_skill_power(
                        sp_pk,
                        reactor["reactor_id"],
                        lvl,
                        sp["skill_atk_power"],
                        sp["sub_skill_atk_power"]
                    )

                # -- coefficients
                for coeff in sp.get("skill_power_coefficient", []):
                    coeff_stat_id = stats_dict[coeff["coefficient_stat_id"]]
                    coeff_pk = crud_reactors.get_reactor_coeff(
                        reactor["reactor_id"], lvl, coeff_stat_id
                    )
                    if coeff_pk is None:
                        crud_reactors.add_reactor_coeff(
                            reactor["reactor_id"], lvl,
                            coeff_stat_id,
                            coeff["coefficient_stat_value"]
                        )
                    else:
                        crud_reactors.update_reactor_coeff(
                            coeff_pk,
                            reactor["reactor_id"], lvl,
                            coeff_stat_id,
                            coeff["coefficient_stat_value"]
                        )

                # -- enchant effects
                for ench in sp.get("enchant_effect", []):
                    ench_stat_id = stats_dict[ench["stat_id"]]
                    ench_pk = crud_reactors.get_reactor_enchant(
                        reactor["reactor_id"], lvl,
                        ench["enchant_level"],
                        ench_stat_id
                    )
                    if ench_pk is None:
                        crud_reactors.add_reactor_enchant(
                            reactor["reactor_id"], lvl,
                            ench["enchant_level"],
                            ench_stat_id,
                            ench["value"]
                        )
                    else:
                        crud_reactors.update_reactor_enchant(
                            ench_pk,
                            reactor["reactor_id"], lvl,
                            ench["enchant_level"],
                            ench_stat_id,
                            ench["value"]
                        )
    finally:
        # Pas de traitement particulier ici
        pass
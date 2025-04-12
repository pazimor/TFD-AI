from request_service import fetch_multy_lang, languages_bdd, get_fixed_lang
from sql.CRUD.translation_strings import parse_for_languages

STATISTICS_URL = "stat.json"

def fetch_statistics():
    try:
        stats = fetch_multy_lang(STATISTICS_URL)

        indexed_stats = {}
        for lang in languages_bdd:
            fixed_lang = get_fixed_lang(lang)
            indexed_stats[fixed_lang] = { stat["stat_id"]: stat for stat in stats[fixed_lang] }

        stats_dict = {}
        for stat_id, stat_fr in indexed_stats["fr"].items():
            id_in_DB = 0
            for lang in languages_bdd:
                if lang == "fr":
                    id_in_DB = parse_for_languages("fr", stat_fr["stat_name"])
                    stats_dict[stat_id] = id_in_DB
                    continue
                fixed_lang = get_fixed_lang(lang)
                if stat_id in indexed_stats[fixed_lang]:
                    parse_for_languages(lang, indexed_stats[fixed_lang][stat_id]["stat_name"], id_in_DB)
        return stats_dict
    finally:
        pass

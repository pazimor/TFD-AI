from request_service import fetch_multy_lang, languages_bdd, get_fixed_lang
from sql.CRUD.translation_strings import parse_for_languages
from sql.CRUD import modules as crud_module
import re
import json

MODULE_URL = "module.json"

_NUM_RE = re.compile(r'([+\-＋－]?\d+(?:[.,]\d+)?\s*(?:%|％)?)')
_OP_RE  = re.compile(r'\[(?P<op>[+x×÷*/\-])\]')

def normalise_effect(raw: str):
    idx = 1
    amounts = []

    def _sub(m):
        nonlocal idx
        amounts.append(m.group(1).strip())
        placeholder = f"{{{idx}}}"
        idx += 1
        return placeholder

    txt = raw.replace('\u00A0', ' ').strip(" .")
    m_op = _OP_RE.search(txt)
    op = m_op.group("op") if m_op else None
    if m_op:
        txt = txt.replace(m_op.group(0), "")  # retire [+]
    name_norm = _NUM_RE.sub(_sub, txt).strip()
    return name_norm, amounts, op

def split_effects(module: dict, all_modules) -> list[dict]:
    indexed = {
        get_fixed_lang(lang): {
            mod["module_id"]: mod for mod in all_modules[get_fixed_lang(lang)]
        }
        for lang in languages_bdd
    }

    results: list[dict] = []
    for idx, stat_fr in enumerate(module.get("module_stat")):
        raw_fr = stat_fr.get("value", "") or ""

        name_norm, amounts, op = normalise_effect(raw_fr)
        name_id = parse_for_languages("fr", name_norm)

        for lang in languages_bdd:
            if lang == "fr":
                continue
            fixed = get_fixed_lang(lang)
            mod_tr = indexed.get(fixed, {}).get(module["module_id"])
            if not mod_tr:
                continue
            stats_tr = mod_tr.get("module_stat", [])
            if idx < len(stats_tr):
                raw_tr = stats_tr[idx].get("value", "") or ""
                name_norm, amounts, op = normalise_effect(raw_tr)
                parse_for_languages(lang, name_norm, name_id)

        results.append({
            "name_id": name_id,
            "amount": amounts,
            "op": op,
        })

    return results


def fetch_modules():
    try:
        all_modules = fetch_multy_lang(MODULE_URL)

        # On instancie les langues si nécessaire
        for lang in languages_bdd:
            parse_for_languages(get_fixed_lang(lang), None, 1)

        # Index pour accès O(1) par module_id dans chaque langue
        indexed = {
            get_fixed_lang(lang): {m["module_id"]: m for m in all_modules[get_fixed_lang(lang)]}
            for lang in languages_bdd
        }

        # Boucle principale : on part du FR (référence de l’ID de traduction)
        for m in all_modules["fr"]:
            # ---------- Traductions principales ----------
            id_name   = parse_for_languages("fr", m["module_name"])
            id_type   = parse_for_languages("fr", m["module_type"])
            id_socket = parse_for_languages("fr", m["module_socket_type"])
            id_class  = parse_for_languages("fr", m["module_class"])

            weapon_type_ids = [parse_for_languages("fr", wt) for wt in m.get("available_weapon_type", [])]
            slot_type_ids   = [parse_for_languages("fr", st) for st in m.get("available_module_slot_type", [])]

            # ---------- Autres langues ----------
            for lang in languages_bdd:
                if lang == "fr":
                    continue
                fixed = get_fixed_lang(lang)
                trans = indexed[fixed].get(m["module_id"])
                if not trans:

                    continue
                parse_for_languages(fixed, trans["module_name"],           id_name)
                parse_for_languages(fixed, trans["module_type"],           id_type)
                parse_for_languages(fixed, trans["module_socket_type"],    id_socket)
                parse_for_languages(fixed, trans["module_class"],          id_class)

                for pos, wt in enumerate(trans.get("available_weapon_type", [])):
                    parse_for_languages(fixed, wt, weapon_type_ids[pos])

                for pos, st in enumerate(trans.get("available_module_slot_type", [])):
                    parse_for_languages(fixed, st, slot_type_ids[pos])

            # ---------- Insert / update module ----------
            db_pk = crud_module.get_module(m["module_id"])
            available_weapon_type     = ",".join(map(str, weapon_type_ids)) if weapon_type_ids else None
            available_descendant_id   = ",".join(m.get("available_descendant_id", [])) or None
            available_module_slot_type = ",".join(map(str, slot_type_ids)) if slot_type_ids else None

            if db_pk is None:
                crud_module.add_module(
                    id_name, m["module_id"], m["image_url"], id_type, m["module_tier_id"],
                    id_socket, id_class, available_weapon_type,
                    available_descendant_id, available_module_slot_type
                )
            else:
                crud_module.update_module(
                    db_pk, id_name, m["module_id"], m["image_url"], id_type, m["module_tier_id"],
                    id_socket, id_class, available_weapon_type,
                    available_descendant_id, available_module_slot_type
                )

            # ---------- Statistiques par niveau ----------
            current_module_stats = split_effects(m, all_modules)
            stats_list = m.get("module_stat", [])
            num_levels = len(stats_list)
            stats_per_level = len(current_module_stats) // num_levels if num_levels > 0 else 0

            for idx, s in enumerate(stats_list):
                level = s.get("level", 0)
                capacity = s.get("module_capacity", 0)

                # get all stats
                start = idx * stats_per_level
                end = start + stats_per_level
                slice_stats = current_module_stats[start:end]
                effects_json = json.dumps(slice_stats, ensure_ascii=False)

                stat_pk = crud_module.get_module_stat(m["module_id"], level)
                if stat_pk is None:
                    crud_module.add_module_stat(m["module_id"], level, capacity, effects_json)
                else:
                    crud_module.update_module_stat(stat_pk, m["module_id"], level, capacity, effects_json)
    finally:
        pass
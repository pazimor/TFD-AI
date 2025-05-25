import json

import requests
from sql.CRUD.board_groups import upsert_board_groups
from sql.CRUD.board_nodes import upsert_board_nodes
from sql.CRUD.nodes import upsert_nodes, get_nodes_by_id
from sql.CRUD.boards import upsert_boards
from sql.CRUD.node_effects import upsert_node_effects
from sql.CRUD.translation_strings import parse_for_languages
from request_service import fetch_url, fetch_multy_lang, languages, languages_bdd, get_fixed_lang

BASE_URL = "https://open.api.nexon.com/static/tfd/meta"
# URL de base (ne dépend plus d'une langue)
GROUPS_URL = "arche-tuning-board-group.json"
BOARD_URL = "arche-tuning-board.json"
NODE_URL = "arche-tuning-node.json"
STATISTICS_URL = "stat.json"

def fill_archeron():

    groups = fetch_url(f"{BASE_URL}/{GROUPS_URL}")
    boards = fetch_url(f"{BASE_URL}/{BOARD_URL}")
    stats = fetch_multy_lang(STATISTICS_URL)
    nodes = fetch_multy_lang(NODE_URL)

    indexed_stats = {}
    indexed_nodes = {}
    for lang in languages_bdd:
        fixed_lang = get_fixed_lang(lang)
        indexed_stats[fixed_lang] = {stat["stat_id"]: stat for stat in stats[fixed_lang]}
        indexed_nodes[fixed_lang] = {node["node_id"]: node for node in nodes[fixed_lang]}

    i = 0
    for node in nodes["fr"]:
        node_id = get_nodes_by_id(node["node_id"])
        if node.get("node_effect") is not None:
            for effect in node["node_effect"]:
                id_in_DB = parse_for_languages("fr", indexed_stats["fr"][effect["stat_id"]]["stat_name"])
                upsert_node_effects(None, node["node_id"], id_in_DB, effect["stat_value"], effect["operator_type"])
                i = i + 1
        if node_id == -1:
            print("test: ", node["node_name"])
            id_in_DB = parse_for_languages("fr", node["node_name"])
            upsert_nodes(node["node_id"], id_in_DB, node["node_image_url"], node["node_type"], node["tier_id"], node["required_tuning_point"])

    for board in boards:
        board_id = upsert_boards(board["arche_tuning_board_id"], board["row_size"], board["column_size"])
        for node in board["node"]:
            ## TODO: manage effect later
            upsert_board_nodes(-1, board_id, node["node_id"], node["position_row"], node["position_column"])

    i = 0
    for group in groups:
        upsert_board_groups(i, group["arche_tuning_board_group_id"], group["descendant_group_id"], group["arche_tuning_board_id"])
        i = i + 1

    print("FINI")
    return (groups, board, node)
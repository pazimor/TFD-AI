import threading
import json

from flask import Flask, jsonify, request
from fillroutes.full  import full
from flask_cors import CORS
from sql.CRUD import user, ui

app = Flask(__name__)

CORS(app)
CORS(app, resource={r"/api/*": {"origins": "http://localhost:4200"}}, supports_credentials=True)
CORS(app, supports_credentials=True, methods=["GET", "POST"], allow_headers=["Content-Type"])

@app.route('/api/user_settings', methods=['POST'])
def get_user_settings():
    try:
        user.sync_user(request.json)
        settings = user.fetch_settings(request.json['id'])
        return jsonify({"success": True, "settings": settings or {}}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/set_settings', methods=['POST'])
def set_user_settings():
    try:
        settings = user.set_user_settings(request.json['id'], request.json['lang'])
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/modules', methods=['GET'])
def get_modules():
    data = ui.get_all_modules()
    for module in data:
        stats_raw = module.get("stats")
        if isinstance(stats_raw, str):
                module["stats"] = json.loads(stats_raw)

    return app.response_class(
        json.dumps(data, ensure_ascii=False),
        mimetype="application/json"
    )

@app.route('/api/translations', methods=['GET'])
def get_translations():
    data = ui.get_all_translations()
    return app.response_class(
        json.dumps(data, ensure_ascii=False),
        mimetype="application/json"
    )

@app.route('/api/descendants', methods=['GET'])
def api_get_descendants_full():
    data = ui.get_all_descendants()
    return app.response_class(
        json.dumps(data, ensure_ascii=False),
        mimetype="application/json"
    )


@app.route('/api/weapons', methods=['GET'])
def api_get_weapons_full():
    data = ui.get_all_weapons_full()
    return app.response_class(
        json.dumps(data, ensure_ascii=False),
        mimetype="application/json"
    )

@app.route('/api/cores/<int:weapon_id>', methods=['GET'])
def api_weapon_core_slots(weapon_id):
    data = ui.get_weapon_core_slots(weapon_id)
    return app.response_class(
        json.dumps(data, ensure_ascii=False),
        mimetype="application/json"
    )

@app.route('/api/external-components', methods=['GET'])
def api_get_external_components_full():
    data = ui.get_all_external_components_full()
    return app.response_class(
        json.dumps(data, ensure_ascii=False),
        mimetype="application/json"
    )

@app.route('/api/reactors', methods=['GET'])
def api_get_reactors_full():
    data = ui.get_all_reactors_full()
    return app.response_class(
        json.dumps(data, ensure_ascii=False),
        mimetype="application/json"
    )

@app.route('/api/boards', methods=['GET'])
def api_get_boards_full():
    data = ui.get_all_boards_full()
    return app.response_class(
        json.dumps(data, ensure_ascii=False),
        mimetype="application/json"
    )

@app.route('/bdd/import_data', methods=['GET'])
def import_data():
    try:
        weapon = False
        statistic = False
        core = False
        descendant = False
        module = False
        reactor = False
        external = False
        archerons = True

        thread = threading.Thread(target=full, args=(weapon, statistic, core, descendant, module, reactor, external))
        thread.start()

        return jsonify({"success": True, "message": "importing data"}), 202
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4201)
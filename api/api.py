import threading
from os import supports_bytes_environ

import requests
import json

from flask import Flask, jsonify, request
from fillroutes.full  import full
from flask_cors import CORS
from sql.CRUD import user

app = Flask(__name__)

CORS(app)
CORS(app, resource={r"/api/*": {"origins": "http://localhost:4200"}}, supports_credentials=True)
CORS(app, supports_credentials=True, methods=["GET", "POST"], allow_headers=["Content-Type"])

@app.route('/api/user_settings', methods=['POST'])
def get_user_settings():
    try:

        print(request.json, flush=True)

        # Sync user in DB
        user.sync_user(request.json)

        # Fetch user settings
        settings = user.fetch_settings(request.json['id'])
        return jsonify({"success": True, "settings": settings or {}}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/set_settings', methods=['POST'])
def set_user_settings():
    try:

        print(request.json, flush=True)

        # Fetch user settings
        settings = user.set_user_settings(request.json['id'], request.json['lang'])
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/bdd/import_data', methods=['GET'])
def import_data():
    try:
        weapon = False
        statistic = True
        core = False
        descendant = False
        module = False
        reactor = False
        external = True

        thread = threading.Thread(target=full, args=(weapon, statistic, core, descendant, module, reactor, external))
        thread.start()

        return jsonify({"success": True, "message": "importing data"}), 202
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4201)
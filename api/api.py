from flask import Flask, jsonify
from flask_cors import CORS
import json
import sql.crud as crud
app = Flask(__name__)

CORS(app)
# CORS(app, origins=["http://localhost:4200"])
# CORS(app, supports_credentials=True, methods=["GET", "POST"], allow_headers=["Content-Type"])

@app.route('/api/modules/ui', methods=['GET'])
def get_module_for_ui():
    data = crud.get_modifiers_by_type("Module")
    # Définition des clés correspondant aux colonnes de la table SQL
    keys = ["id", "type", "statistiques", "optional_statistiques", "stack_id", "stack_description", "display_data", "name"]

    result = []
    for row in data:
        row_dict = dict(zip(keys, row))
        if "name" in row_dict and isinstance(row_dict["name"], str):
            try:
                row_dict["name"] = json.loads(row_dict["name"])
            except json.JSONDecodeError:
                pass  # Laisser tel quel si ce n'est pas un JSON valide
        if "statistiques" in row_dict and isinstance(row_dict["statistiques"], str):
            try:
                row_dict["statistiques"] = json.loads(row_dict["statistiques"])
            except json.JSONDecodeError:
                print("pas cool")
                pass  # Laisser tel quel si ce n'est pas un JSON valide
        if "display_data" in row_dict and isinstance(row_dict["display_data"], str):
            try:
                row_dict["display_data"] = json.loads(row_dict["display_data"])
            except json.JSONDecodeError:
                pass  # Laisser tel quel si ce n'est pas un JSON valide

        result.append(row_dict)

    return jsonify(result)

@app.route('/api/descendants/ui', methods=['GET'])
def get_descendants_for_ui():
    data = crud.get_items_by_type("descendant")
    keys = ["id", "name", "type", "goals", "capabilities", "statistiques", "display_data"]

    result = []
    for row in data:
        row_dict = dict(zip(keys, row))
        #TODO: implement name later
        if "name" in row_dict and isinstance(row_dict["name"], str):
            try:
                row_dict["name"] = json.loads(row_dict["name"])
            except json.JSONDecodeError:
                pass  # Laisser tel quel si ce n'est pas un JSON valide
        if "capabilities" in row_dict and isinstance(row_dict["capabilities"], str):
            try:
                row_dict["capabilities"] = json.loads(row_dict["capabilities"])
            except json.JSONDecodeError:
                pass  # Laisser tel quel si ce n'est pas un JSON valide
        if "display_data" in row_dict and isinstance(row_dict["display_data"], str):
            try:
                row_dict["display_data"] = json.loads(row_dict["display_data"])
            except json.JSONDecodeError:
                pass  # Laisser tel quel si ce n'est pas un JSON valide

        result.append(row_dict)

    return jsonify(result)

@app.route('/api/weapons/ui', methods=['GET'])
def get_weapons_for_ui():
    data = crud.get_items_by_type("weapon")
    keys = ["id", "name", "type", "goals", "capabilities", "statistiques", "display_data"]

    result = []
    for row in data:
        row_dict = dict(zip(keys, row))
        #TODO: implement name later
        if "name" in row_dict and isinstance(row_dict["name"], str):
            try:
                row_dict["name"] = json.loads(row_dict["name"])
            except json.JSONDecodeError:
                pass  # Laisser tel quel si ce n'est pas un JSON valide
        if "capabilities" in row_dict and isinstance(row_dict["capabilities"], str):
            try:
                row_dict["capabilities"] = json.loads(row_dict["capabilities"])
            except json.JSONDecodeError:
                pass  # Laisser tel quel si ce n'est pas un JSON valide
        if "display_data" in row_dict and isinstance(row_dict["display_data"], str):
            try:
                row_dict["display_data"] = json.loads(row_dict["display_data"])
            except json.JSONDecodeError:
                pass  # Laisser tel quel si ce n'est pas un JSON valide

        result.append(row_dict)

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4201)
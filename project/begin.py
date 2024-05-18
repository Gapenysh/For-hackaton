from project import app
from flask import Flask, request, jsonify
import sqlite3
from project.user_model import RefactData

@app.route('/landmarks', methods=["POST", "GET"])
def get_landmarks_from_id():
    id = request.json.get("id", None)
    data = None
    if id != None:
        data = RefactData.refactor_data_to_json_from_id(id)
        print(data)
        return jsonify({"message": "Good!",
                        "data": data})
    else:
        print("Ошибка в получении данных от фронтенда(id)")
        return jsonify({"message": "Bad!",
                        "data": data})

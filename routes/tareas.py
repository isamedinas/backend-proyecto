from flask import Blueprint, request, jsonify
from config.db import get_db_connection

tareas_bp = Blueprint('tareas', __name__)

@tareas_bp.route('/obtener', methods=['GET'])
def obtener_tareas():
    cursor = get_db_connection()
    cursor.execute("SELECT * FROM tareas")
    tareas = cursor.fetchall()
    cursor.close()
    return jsonify(tareas), 200

@tareas_bp.route('/crear', methods=['POST'])
def crear_tarea():
    data = request.get_json()
    descripcion = data.get('description')

    if not descripcion:
        return jsonify({"error": "Falta la descripción"}), 400

    cursor = get_db_connection()
    try:
        cursor.execute("INSERT INTO tareas (descripcion) VALUES (%s)", (descripcion,))
        cursor.connection.commit()
        return jsonify({"message": "Tarea creada"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

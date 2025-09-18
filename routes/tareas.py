from flask import Blueprint, request, jsonify
from routes import get_db_connection

#Blueprint
tareas_bp = Blueprint('tareas', __name__)

#Crear un endopoint obtener tareas

@tareas_bp.route('/obtener', methods=['GET'])
def get():
    return jsonify({"mensaje": "Estas son tus tareas"})

# Endpoint recibiendo del body

@tareas_bp.route('/crear', methods=['POST'])
def crear():
    # Obtenemos el body
    data = request.get_json()
    descripcion = data.get('description')

    if not descripcion:
        return jsonify({"error": "Necesitas una descripcion"}), 400

    # Obtenemos el cursor
    cursor = get_db_connection()

    # Hacemos el insert
    try:
        cursor.execute(
            'INSERT INTO tareas (descripcion) values (%s)', (descripcion,))
        cursor.connection.commit()
        return jsonify({"message": "tarea creada"}), 201
    except Exception as e:
        return jsonify({"Error": f"No se pudo crear la tarea: {str(e)}"}), 400
    finally:
        cursor.close()


@tareas_bp.route("/modificar/<int:user_id>", methods=["PUT"])
def modificar(user_id):
    data = request.get_json()

    nombre = data.get('nombre')
    apellido = data.get("apellido")

    mensaje = f"Usuario con id: {user_id} y nombre: {nombre} {apellido}"

    return jsonify({"saludo": f"Hola {nombre} {apellido} como estas"})
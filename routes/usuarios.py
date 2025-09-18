from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
import datetime

from routes import get_db_connection

from dotenv import load_dotenv

load_dotenv()

usuarios_bp = Blueprint('usuarios', __name__)

# iniciar el bcryprt
bcrypt = Bcrypt()


@usuarios_bp.route('/registrar', methods=['POST'])
def registrar():
    # body de datos
    data = request.get_json()

    nombre = data.get('nombre')
    email = data.get('email')
    password = data.get('password')

    # validar
    if not nombre or not email or not password:
        return jsonify({"error": "Faltan datos"}), 400

    # cursos base de datos
    cursor = get_db_connection()

    try:
        # que no exista el usuario
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            return jsonify({"error": "Ese usuario ya existe"}), 400

        # hash passwod
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Insertar registro a la base
        cursor.execute('''INSERT INTO usuarios (nombre, email, password) values (%s,%s,%s)''',
                       (nombre, email, hashed_password))

        # nuevo registro
        cursor.connection.commit()

        return jsonify({"mensaje": "El usuario se creo correctamente"}), 201

    except Exception as e:
        return jsonify({"error": f"Error al registrar al usuario: {str(e)}"}), 500

    finally:
        # cerrar el cursor
        cursor.close()


@usuarios_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Faltan datos"}), 400

    cursor = get_db_connection()

    query = "SELECT password, id_usuario FROM usuarios WHERE email = %s"
    cursor.execute(query, (email,))

    usuario = cursor.fetchone()

    if usuario and bcrypt.check_password_hash(usuario[0], password):
        #generamos el JWT
        expires = datetime.timedelta(minutes=60)

        acces_token = create_access_token(
            identity=str(usuario[1]),
            expires_delta=expires
        )
        cursor.close()
        return jsonify({"access_token": acces_token}), 200
    else:
        return jsonify({"error": "Credenciales Incorrectas"}), 401


@usuarios_bp.route('/datos', methods=['GET'])
@jwt_required()
def datos():
    current_user = get_jwt_identity()

    cursor = get_db_connection()

    query = "SELECT id_usuario, nombre, email FROM USUARIOS where id_usuario = %s"
    cursor.execute(query, (current_user,))
    usuario = cursor.fetchone()

    cursor.close()

    if usuario:
        user_info = {
            "id_usuario": usuario[0],
            "nombre": usuario[1],
            "email": usuario[2],
        }
        return jsonify({"datos": user_info}), 200
    else:
        return jsonify({"error": "Usuario no encontrado"}), 404
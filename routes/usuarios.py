from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from config.db import get_db_connection
import datetime

usuarios_bp = Blueprint('usuarios', __name__)
bcrypt = Bcrypt()

@usuarios_bp.route('/registrar', methods=['POST'])
def registrar():
    data = request.get_json()
    nombre = data.get('nombre')
    email = data.get('email')
    password = data.get('password')

    if not nombre or not email or not password:
        return jsonify({"error": "Faltan datos"}), 400

    cursor = get_db_connection()
    cursor.execute("SELECT * FROM usuarios WHERE email=%s", (email,))
    if cursor.fetchone():
        cursor.close()
        return jsonify({"error": "Usuario ya existe"}), 400

    hashed = bcrypt.generate_password_hash(password).decode('utf-8')
    cursor.execute("INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)",
                   (nombre, email, hashed))
    cursor.connection.commit()
    cursor.close()

    return jsonify({"mensaje": "Usuario creado"}), 201

@usuarios_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Faltan datos"}), 400

    cursor = get_db_connection()
    cursor.execute("SELECT id_usuario, password FROM usuarios WHERE email=%s", (email,))
    usuario = cursor.fetchone()
    cursor.close()

    if usuario and bcrypt.check_password_hash(usuario["password"], password):
        token = create_access_token(
            identity=usuario["id_usuario"],
            expires_delta=datetime.timedelta(hours=1)
        )
        return jsonify({"access_token": token}), 200
    return jsonify({"error": "Credenciales incorrectas"}), 401

@usuarios_bp.route('/datos', methods=['GET'])
@jwt_required()
def datos():
    current_user = get_jwt_identity()
    cursor = get_db_connection()
    cursor.execute("SELECT id_usuario, nombre, email FROM usuarios WHERE id_usuario=%s", (current_user,))
    usuario = cursor.fetchone()
    cursor.close()

    if usuario:
        return jsonify(usuario), 200
    return jsonify({"error": "Usuario no encontrado"}), 404

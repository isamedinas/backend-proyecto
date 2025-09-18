from flask import Flask
import os
from dotenv import load_dotenv
from config.db import init_db, mysql
from flask_jwt_extended import JWTManager

from routes.tareas import tareas_bp
from routes.usuarios import usuarios_bp

load_dotenv()

def create_app():
    app = Flask(__name__)
    init_db(app)

    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET')
    jwt = JWTManager(app)

    # Registrar blueprints
    app.register_blueprint(tareas_bp, url_prefix="/tareas")
    app.register_blueprint(usuarios_bp, url_prefix='/usuarios')

    return app

# esta es la variable que gunicorn usa
app = create_app()

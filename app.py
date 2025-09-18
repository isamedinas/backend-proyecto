from flask import Flask
import os
from dotenv import load_dotenv
from config.db import init_db
from flask_jwt_extended import JWTManager

# Rutas (blueprints)
from routes.tareas import tareas_bp
from routes.usuarios import usuarios_bp

# Cargar variables de entorno
load_dotenv()

def create_app():
    app = Flask(__name__)
    init_db(app)

    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET', 'secret-key')
    JWTManager(app)

    # Registrar rutas
    app.register_blueprint(tareas_bp, url_prefix="/tareas")
    app.register_blueprint(usuarios_bp, url_prefix="/usuarios")

    return app

# Instancia de la app
app = create_app()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)

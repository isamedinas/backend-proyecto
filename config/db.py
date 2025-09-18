from flask_mysql_connector import MySQL
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Crear instancia de MySQL
mysql = MySQL()

def init_db(app):
    """
    Configura la conexión a la base de datos MySQL
    usando las variables de entorno definidas en Railway.
    """
    app.config['MYSQL_HOST'] = os.getenv("DB_HOST", "localhost")
    app.config['MYSQL_USER'] = os.getenv("DB_USER", "root")
    app.config['MYSQL_PASSWORD'] = os.getenv("DB_PASSWORD", "")
    app.config['MYSQL_DATABASE'] = os.getenv("DB_NAME", "mi_base")
    app.config['MYSQL_PORT'] = int(os.getenv("DB_PORT", 3306))

    # Inicializamos la conexión
    mysql.init_app(app)


def get_db_connection():
    """
    Devuelve un cursor activo para interactuar con la base de datos.
    """
    try:
        connection = mysql.connection
        cursor = connection.cursor(dictionary=True)  # Devuelve resultados como diccionarios
        return cursor
    except Exception as e:
        raise RuntimeError(f"Error al conectar a la base de datos: {e}")

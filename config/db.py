from flask_mysql_connector import MySQL
import os
from dotenv import load_dotenv

load_dotenv()

mysql = MySQL()

def init_db(app):
    """Configura la conexión a MySQL usando variables de entorno"""
    app.config['MYSQL_HOST'] = os.getenv("DB_HOST", "localhost")
    app.config['MYSQL_USER'] = os.getenv("DB_USER", "root")
    app.config['MYSQL_PASSWORD'] = os.getenv("DB_PASSWORD", "")
    app.config['MYSQL_DATABASE'] = os.getenv("DB_NAME", "mi_base")
    app.config['MYSQL_PORT'] = int(os.getenv("DB_PORT", 3306))
    mysql.init_app(app)

def get_db_connection():
    """Devuelve un cursor para consultas a la BD"""
    connection = mysql.connection
    return connection.cursor(dictionary=True)

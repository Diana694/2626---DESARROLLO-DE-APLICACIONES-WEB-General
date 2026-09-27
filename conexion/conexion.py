import os
import psycopg2
from psycopg2.extras import RealDictCursor

def obtener_conexion():
    try:
        # Render asigna automáticamente la URL de la BD en la variable DATABASE_URL
        database_url = os.environ.get('DATABASE_URL')
        
        if database_url:
            # Corrección de protocolo por compatibilidad con psycopg2
            if database_url.startswith("postgres://"):
                database_url = database_url.replace("postgres://", "postgresql://", 1)
            conexion = psycopg2.connect(database_url, cursor_factory=RealDictCursor)
        else:
            # Conexión local de respaldo para PostgreSQL
            conexion = psycopg2.connect(
                host=os.environ.get('DB_HOST', 'localhost'),
                user=os.environ.get('DB_USER', 'postgres'),
                password=os.environ.get('DB_PASSWORD', 'admin123'),
                dbname=os.environ.get('DB_NAME', 'panaderia_db'),
                port=os.environ.get('DB_PORT', '5432'),
                cursor_factory=RealDictCursor
            )
        return conexion
    except Exception as e:
        print(f"Error al conectar a PostgreSQL: {e}")
        return None
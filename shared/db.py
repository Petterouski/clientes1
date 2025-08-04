# shared/db.py
import psycopg2

def get_connection():
    return psycopg2.connect(
        host="database-1.c8mycxjkbhzn.us-east-1.rds.amazonaws.com",     # o 127.0.0.1    localhost
        database="postgres",  # nombre de la base de datos clientes_db para el localhost
        user="postgres",      # tu usuario de PgAdmin
        password="admin123",  # tu contraseña de PgAdmin para local solo admin
        port="5432"           # puerto por defecto de PostgreSQL
    )

import sys
import os
from flask import Flask, jsonify
from flask_cors import CORS  # ✅ Importar CORS

# prueba 2 CI/CD
# Configuración de rutas
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from shared.db import get_connection

app = Flask(__name__)
CORS(app)  # ✅ Habilitar CORS

@app.route('/')
def home():
    return "Microservicio activo. GET en /read_clients"

@app.route('/read_clients', methods=['GET'])
def read_clients():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, ci, nombres, apellidos, telefono, correo FROM clientes")
        rows = cur.fetchall()

        # Convertir a lista de diccionarios
        result = [
            {
                "id": row[0],
                "ci": row[1],
                "nombres": row[2],
                "apellidos": row[3],
                "telefono": row[4],
                "correo": row[5]
            }
            for row in rows
        ]

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

if __name__ == '__main__':
    app.run(debug=True, port=5002, host='0.0.0.0')  # ✅ host agregado
import sys
import os
from flask import Flask, jsonify
from flask_cors import CORS  # Importar CORS

# Configuración
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from shared.db import get_connection

app = Flask(__name__)
CORS(app)  # ✅ Habilitar CORS

@app.route('/')
def home():
    return "Microservicio activo. DELETE en /delete_client/<id>"

@app.route('/delete_client/<int:id>', methods=['DELETE'])
def delete_client(id):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM clientes WHERE id = %s", (id,))
        conn.commit()

        if cur.rowcount == 0:
            return jsonify({"mensaje": "Cliente no encontrado"}), 404
        return jsonify({"mensaje": "Cliente eliminado"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if 'cur' in locals():  # ✅ Manejo seguro
            cur.close()
        if 'conn' in locals():
            conn.close()

if __name__ == '__main__':
    app.run(debug=True, port=5004, host='0.0.0.0')  # ✅ host agregado

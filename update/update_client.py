import sys
import os
from flask import Flask, request, jsonify
from flask_cors import CORS  # ✅ Importar CORS

# Configurar rutas de importación
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from shared.db import get_connection

app = Flask(__name__)
CORS(app)  # ✅ Habilitar CORS

@app.route('/')
def home():
    return "Microservicio activo. PUT en /update_client/<id>"

@app.route('/update_client/<int:id>', methods=['PUT'])
def update_client(id):
    # ✅ Validar tipo de contenido
    if request.content_type != 'application/json':
        return jsonify({
            "error": "Unsupported Media Type: Se requiere 'application/json'"
        }), 415

    data = request.get_json()

    if not data:
        return jsonify({"error": "Datos JSON requeridos"}), 400

    required_fields = ['ci', 'nombres', 'apellidos', 'telefono', 'correo']
    missing = [field for field in required_fields if field not in data]
    if missing:
        return jsonify({"error": f"Faltan campos: {', '.join(missing)}"}), 400

    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE clientes
            SET ci = %s, nombres = %s, apellidos = %s, telefono = %s, correo = %s
            WHERE id = %s
        """, (
            data['ci'],
            data['nombres'],
            data['apellidos'],
            data['telefono'],
            data['correo'],
            id
        ))

        conn.commit()
        if cur.rowcount == 0:
            return jsonify({"mensaje": "Cliente no encontrado"}), 404
        return jsonify({"mensaje": "Cliente actualizado"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

if __name__ == '__main__':
    app.run(debug=True, port=5003, host='0.0.0.0')  # ✅ host agregado
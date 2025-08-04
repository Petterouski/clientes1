import sys
import os
from flask import Flask, request, jsonify
from flask_cors import CORS  # Importa CORS

# Configurar rutas de importación
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from shared.db import get_connection

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas las rutas

@app.route('/')
def home():
    return "Microservicio activo. Usa POST en /create_client"

@app.route('/create_client', methods=['POST'])
def create_client():
    # Verificar el tipo de contenido
    if request.content_type != 'application/json':
        return jsonify({
            "error": "Unsupported Media Type: Se requiere 'application/json'"
        }), 415
    
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Datos JSON requeridos"}), 400
        
    required_fields = ['ci', 'nombres', 'apellidos', 'telefono', 'correo']
    if missing := [field for field in required_fields if field not in data]:
        return jsonify({"error": f"Faltan campos: {', '.join(missing)}"}), 400

    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO clientes (ci, nombres, apellidos, telefono, correo) VALUES (%s, %s, %s, %s, %s)",
            (data['ci'], data['nombres'], data['apellidos'], data['telefono'], data['correo'])
        )
        conn.commit()
        return jsonify({
            "mensaje": "Cliente creado",
            "id": cur.lastrowid  # Devuelve el ID generado
        }), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
    finally:
        if 'cur' in locals(): cur.close()
        if 'conn' in locals(): conn.close()

if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')

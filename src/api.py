"""
Path: src/api.py
"""

from flask import Blueprint, jsonify

api_bp = Blueprint("api", __name__, url_prefix="/api")

@api_bp.route("/data", methods=["GET"])
def fetch_data():
    try:
        # Lógica para obtener datos de la base de datos.
        # Por ahora se retorna un dato de ejemplo.
        data = [{"id": 1, "valor": "ejemplo"}]
        return jsonify(status="success", data=data), 200
    except Exception as e:
        # Manejo básico de errores.
        return jsonify(status="error", message=str(e)), 500
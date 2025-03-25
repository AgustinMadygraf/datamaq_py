"""
Path: src/main_flask.py
"""

from flask import Flask, render_template, jsonify
from src.db_operations import SQLAlchemyDatabaseRepository

app = Flask(__name__, template_folder="views")

@app.route("/PanelControlModbus")
def panel_control():
    return render_template("PanelControlModbus.html")

@app.route("/")
def index():
    return render_template("index.html")

def fetch_data_from_db():
    """Extrae la lógica de consulta a la base de datos utilizando SQLAlchemy."""
    db_repo = SQLAlchemyDatabaseRepository()
    consulta = "SELECT * FROM registros_modbus WHERE valor IS NOT NULL"
    parametros = {}
    rows = db_repo.ejecutar_consulta(consulta, parametros)
    # Convertir cada fila a diccionario utilizando _mapping para asegurar JSON serializable
    return [dict(row._mapping) for row in rows]

@app.route("/fetch_data")
def fetch_data():
    try:
        data = fetch_data_from_db()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify(data)

def run():
    app.run(debug=True)


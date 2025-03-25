"""
Path: src/main_flask.py
"""

from flask import Flask, render_template, jsonify
import pymysql

app = Flask(__name__, template_folder="views")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/fetch_data")
def fetch_data():
    try:
        # Ajusta las credenciales según tu entorno
        conn = pymysql.connect(host="localhost", user="root", password="12345678", db="novus",
                               cursorclass=pymysql.cursors.DictCursor)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM registros_modbus WHERE valor IS NOT NULL")
        data = cursor.fetchall()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
    return jsonify(data)

def run():
    app.run(debug=True)


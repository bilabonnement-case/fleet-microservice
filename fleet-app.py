from flask import Flask, jsonify, request
import os
import sqlite3
from datetime import datetime
from dotenv import load_dotenv
from flasgger import Swagger, swag_from

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Swagger Configuration
app.config['SWAGGER'] = {
    'title': 'Fleet Microservice API',
    'uiversion': 3,
    'openapi': '3.0.0'
}
swagger = Swagger(app)

# Database Opsætning
DATABASE = "fleet-database.db"


def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()

        # Drop tabellen hvis nødvendigt
        # cursor.execute("DROP TABLE IF EXISTS fleet")

        # Opret fleet tabellen
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS fleet (
            bil_id INTEGER PRIMARY KEY AUTOINCREMENT,
            stelnummer TEXT NOT NULL,
            abonnement_id INTEGER,
            mærke TEXT NOT NULL,
            model TEXT NOT NULL,
            månedlig_pris REAL NOT NULL,
            kilometer_grænse INTEGER NOT NULL,
            kilometerafstand INTEGER,
            registreringsnummer TEXT NOT NULL,
            status TEXT NOT NULL,
            admin_id INTEGER NOT NULL
        )
        """)
        conn.commit()


init_db()

# Enum for Bil Status
class BilStatus:
    TILGÆNGELIG = "Tilgængelig"
    UDLEJET = "Udlejet"
    UNDER_VEDLIGEHOLD = "Under vedligehold"
    UDGÅET = "Udgået"


@app.route('/')
@swag_from('swagger/home.yaml')
def home():
    return jsonify({
        "service": "Fleet-Service",
        "available_endpoints": [
            {"path": "/create_vehicle", "method": "POST", "description": "Opret ny bil i flåden"},
            {"path": "/get_vehicle/<int:bil_id>", "method": "GET", "description": "Hent bil detaljer baseret på bil ID"},
            {"path": "/update_vehicle/<int:bil_id>", "method": "PUT", "description": "Opdater en bils detaljer"},
            {"path": "/delete_vehicle/<int:bil_id>", "method": "DELETE", "description": "Slet en bil fra flåden"},
            {"path": "/list_vehicles", "method": "GET", "description": "Liste over alle køretøjer i flåden"}
        ]
    })


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/create_vehicle', methods=['POST'])
@swag_from('swagger/create_vehicle.yaml')
def create_vehicle():
    data = request.get_json()

    stelnummer = data['stelnummer']
    abonnement_id = data.get('abonnement_id')
    mærke = data['mærke']
    model = data['model']
    månedlig_pris = data['månedlig_pris']
    kilometer_grænse = data['kilometer_grænse']
    kilometerafstand = data.get('kilometerafstand', 0)
    registreringsnummer = data['registreringsnummer']
    status = data.get('status', BilStatus.TILGÆNGELIG)
    admin_id = data['admin_id']

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO fleet (stelnummer, abonnement_id, mærke, model, månedlig_pris, kilometer_grænse, kilometerafstand, registreringsnummer, status, admin_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (stelnummer, abonnement_id, mærke, model, månedlig_pris, kilometer_grænse, kilometerafstand, registreringsnummer, status, admin_id))
        conn.commit()

    return jsonify({"message": "Køretøj oprettet"}), 201


@app.route('/get_vehicle/<int:bil_id>', methods=['GET'])
@swag_from('swagger/get_vehicle.yaml')
def get_vehicle(bil_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM fleet WHERE bil_id = ?", (bil_id,))
        vehicle = cursor.fetchone()

    if vehicle:
        return jsonify(dict(vehicle)), 200

    return jsonify({"error": "Køretøj ikke fundet"}), 404


@app.route('/update_vehicle/<int:bil_id>', methods=['PUT'])
@swag_from('swagger/update_vehicle.yaml')
def update_vehicle(bil_id):
    data = request.get_json()
    fields = []
    values = []
    for key, value in data.items():
        fields.append(f"{key} = ?")
        values.append(value)

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(f"UPDATE fleet SET {', '.join(fields)} WHERE bil_id = ?", (*values, bil_id))
        conn.commit()

    return jsonify({"message": "Køretøj opdateret"}), 200


@app.route('/delete_vehicle/<int:bil_id>', methods=['DELETE'])
@swag_from('swagger/delete_vehicle.yaml')
def delete_vehicle(bil_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM fleet WHERE bil_id = ?", (bil_id,))
        conn.commit()

    return jsonify({"message": "Køretøj slettet"}), 200


@app.route('/list_vehicles', methods=['GET'])
@swag_from('swagger/list_vehicles.yaml')
def list_vehicles():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM fleet")
        vehicles = cursor.fetchall()

    return jsonify([dict(vehicle) for vehicle in vehicles]), 200


if __name__ == '__main__':
    app.run(debug=bool(int(os.getenv('FLASK_DEBUG', 0))), host='0.0.0.0', port=5005)
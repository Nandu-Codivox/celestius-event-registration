
from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

DATABASE = "registrations.db"
CAPACITY = 50


# Connect to the database
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# Create the registrations table
def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            college TEXT,
            department TEXT,
            registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


# Homepage
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Welcome to Celestius",
        "event": "Backend Development Workshop",
        "capacity": CAPACITY
    })


# Register a student
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Valid JSON data is required"}), 400

    name = data.get("name")
    email = data.get("email")

    if not isinstance(name, str) or not name.strip():
        return jsonify({"error": "Name is required"}), 400

    if not isinstance(email, str) or not email.strip():
        return jsonify({"error": "Email is required"}), 400

    name = name.strip()
    email = email.strip().lower()

    if "@" not in email or "." not in email.split("@")[-1]:
        return jsonify({"error": "Invalid email address"}), 400

    college = data.get("college", "")
    department = data.get("department", "")

    if not isinstance(college, str) or not isinstance(department, str):
        return jsonify({
            "error": "College and department must be text"
        }), 400

    conn = get_db()

    try:
        count = conn.execute(
            "SELECT COUNT(*) FROM registrations"
        ).fetchone()[0]

        if count >= CAPACITY:
            return jsonify({"error": "Event is full"}), 409

        cursor = conn.execute("""
            INSERT INTO registrations
            (name, email, college, department)
            VALUES (?, ?, ?, ?)
        """, (name, email, college.strip(), department.strip()))

        conn.commit()

        student = conn.execute(
            "SELECT * FROM registrations WHERE id = ?",
            (cursor.lastrowid,)
        ).fetchone()

        return jsonify(dict(student)), 201

    except sqlite3.IntegrityError:
        return jsonify({
            "error": "Email is already registered"
        }), 409

    finally:
        conn.close()


# Get all registrations
@app.route("/registrations", methods=["GET"])
def get_registrations():
    conn = get_db()

    try:
        rows = conn.execute(
            "SELECT * FROM registrations ORDER BY id"
        ).fetchall()

        return jsonify({
            "total": len(rows),
            "registrations": [dict(row) for row in rows]
        }), 200

    finally:
        conn.close()


# Get one registration by ID
@app.route("/registrations/<int:registration_id>", methods=["GET"])
def get_registration(registration_id):
    conn = get_db()

    try:
        row = conn.execute(
            "SELECT * FROM registrations WHERE id = ?",
            (registration_id,)
        ).fetchone()

        if row is None:
            return jsonify({"error": "Registration not found"}), 404

        return jsonify(dict(row)), 200

    finally:
        conn.close()


# Get one registration by email
@app.route("/registrations/email/<email>", methods=["GET"])
def get_registration_by_email(email):
    conn = get_db()

    try:
        row = conn.execute(
            "SELECT * FROM registrations WHERE email = ?",
            (email.strip().lower(),)
        ).fetchone()

        if row is None:
            return jsonify({"error": "Registration not found"}), 404

        return jsonify(dict(row)), 200

    finally:
        conn.close()


# Initialize database and start server
if __name__ == "__main__":
    init_db()
    app.run(debug=True)

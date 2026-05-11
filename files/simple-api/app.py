import os
import psycopg2
from flask import Flask, jsonify, request

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_NAME = os.getenv("DB_NAME", "simple_api")
DB_USER = os.getenv("DB_USER", "simple_api_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "simple_api_password")


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/users", methods=["GET"])
def list_users():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM users ORDER BY id")
    users = [{"id": row[0], "name": row[1]} for row in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify(users)


@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    name = data.get("name", "anonymous")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name) VALUES (%s) RETURNING id", (name,))
    user_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"id": user_id, "name": name}), 201


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)

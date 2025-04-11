#  _   _  _____     ____  __ ____ _____ ____
# | \ | |/ _ \ \   / /  \/  | __ )___ /|  _ \
# |  \| | | | \ \ / /| |\/| |  _ \ |_ \| |_) |
# | |\  | |_| |\ V / | |  | | |_) |__) |  _ <
# |_| \_|\___/  \_/  |_|  |_|____/____/|_| \_\
#
# MIT License
#
# Copyright (c) 2024 Daniel Lima
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from contextlib import contextmanager
import sqlite3
from flask import Flask, jsonify, request


app = Flask(__name__)

DB_NAME = "keys.db"
HOST = "0.0.0.0"
PORT = 4321


@contextmanager
def get_conn(db_name: str):
    conn = sqlite3.connect(db_name)
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    with get_conn(DB_NAME) as conn:
        cursor = conn.cursor()
        query = """CREATE TABLE IF NOT EXISTS keys(
        id_key INTEGER PRIMARY KEY AUTOINCREMENT,
        key TEXT,
        machine_id TEXT
        )"""
        cursor.execute(query)


def insert(key: str, machine_id: str):
    with get_conn(DB_NAME) as conn:
        cursor = conn.cursor()
        query = "INSERT INTO keys (key, machine_id) VALUES (?, ?)"
        cursor.execute(query, (key, machine_id))
        conn.commit()


@app.route("/", methods=["POST"])
def recieve_key():
    data = request.get_json(force=True)

    key, machine_id = data.get("key"), data.get("machine_id")
    if not key:
        return jsonify({"error": "Missing key"}), 400

    print(f"[-] Received key: {key}")
    print(f"[-] Machine ID: {machine_id}")

    insert(key, machine_id)

    return jsonify({"message": "Key received successfully"}), 200


@app.route("/list", methods=["GET"])
def list_keys():
    with get_conn(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id_key, key, machine_id FROM keys")
        rows: list[tuple[int, str, str]] = cursor.fetchall()

    data = [{"id": row[0], "key": row[1], "machine_id": row[2]} for row in rows]
    return jsonify(data), 200


if __name__ == "__main__":
    init_db()
    app.run(HOST, PORT)

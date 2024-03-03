# routes.py
import random
import string

import duckdb
from flask import Blueprint, jsonify

from .db import close_db_connection, get_db_connection, open_attach_duckdb

bp = Blueprint('example', __name__)

@bp.route('/users', methods=['GET'])
def get_user():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    data = cursor.fetchall()
    cursor.close()
    close_db_connection(conn)
    return jsonify(data)

@bp.route('/addUser', methods=['GET'])
def add_user():
    username = random_string(10)
    password = random_string(15)
    email = f"{random_string(5)}@example.com"
    sql = """INSERT INTO users (username, password, email) VALUES (%s, %s, %s) RETURNING *;"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql, (username, password, email))
    inserted_user = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    close_db_connection(conn)
    return jsonify(inserted_user)

@bp.route('getDelta', methods=['GET'])
def get_delta():
    # export as parquet
    conn = open_attach_duckdb()
    result = conn.execute("SELECT * FROM postgres_db.users_audit").fetchall()
    conn.close()
    return jsonify(result)

def random_string(length):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

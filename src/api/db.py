# db.py
import duckdb
import psycopg2
from flask import current_app, jsonify
from psycopg2 import pool

import config


def init_db_app(app):
    try:
        app.postgres_pool = psycopg2.pool.SimpleConnectionPool(
            minconn=1, 
            maxconn=10,
            host=app.config['DB_HOST'],
            database=app.config['DB_NAME'],
            user=app.config['DB_USER'],
            password=app.config['DB_PASSWORD'],
            port=app.config['DB_PORT']
        )
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while connecting to PostgreSQL", error)

def get_db_connection():
    if hasattr(current_app, 'postgres_pool'):
        return current_app.postgres_pool.getconn()
    else:
        raise Exception("Database connection pool is not available")

def close_db_connection(conn):
    if hasattr(current_app, 'postgres_pool'):
        current_app.postgres_pool.putconn(conn)
    else:
        raise Exception("Database connection pool is not available")
    
def open_attach_duckdb():
    connection_details = f"host={config.DB_HOST} port={config.DB_PORT} dbname={config.DB_NAME} user={config.DB_USER} password={config.DB_PASSWORD}"
    conn = duckdb.connect(database=':memory:', read_only=False)
    conn.execute(f"ATTACH DATABASE '{connection_details}' AS postgres_db (TYPE 'postgres')")
    return conn
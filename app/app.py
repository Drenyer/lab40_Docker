import time
import psycopg2
from psycopg2 import OperationalError
from flask import Flask, jsonify, g, render_template
import os

app = Flask(__name__)

DATABASE_URL = os.getenv('DATABASE_URL', 'postgres://user:password@db:5432/testdb')

def create_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except OperationalError:
        print("Database not ready, waiting...")
        time.sleep(5)
        return create_connection()

def get_db_connection():
    if 'db_connection' not in g:
        g.db_connection = create_connection()
        g.db_cursor = g.db_connection.cursor()
    return g.db_connection, g.db_cursor

@app.teardown_appcontext
def close_connection(exception):
    db_connection = g.pop('db_connection', None)
    if db_connection is not None:
        db_connection.close()

@app.route('/')
def index():
    conn, cursor = get_db_connection()
    cursor.execute('SELECT * FROM example_table;')
    rows = cursor.fetchall()
    return render_template('index.html', rows=rows)

@app.route('/another')
def get_another_records():
    conn, cursor = get_db_connection()
    cursor.execute('SELECT * FROM another_table;')
    rows = cursor.fetchall()
    return render_template('another.html', rows=rows)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

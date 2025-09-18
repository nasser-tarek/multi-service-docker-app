from flask import Flask, jsonify
import psycopg2
import os
import time

app = Flask(__name__)

# Database connection settings (match docker-compose.yml)
DB_HOST = "db"
DB_NAME = os.getenv("POSTGRES_DB", "mydb")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "postgres")

# Retry until DB is ready
def get_connection():
    while True:
        try:
            conn = psycopg2.connect(
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASS,
                host=DB_HOST
            )
            conn.autocommit = True
            return conn
        except Exception as e:
            print("Database not ready, retrying in 2s...")
            time.sleep(2)

conn = get_connection()
cur = conn.cursor()

# Create table if it doesn’t exist
cur.execute("""
    CREATE TABLE IF NOT EXISTS visits (
        id SERIAL PRIMARY KEY,
        counter INTEGER
    )
""")

# Initialize row if empty
cur.execute("SELECT COUNT(*) FROM visits")
if cur.fetchone()[0] == 0:
    cur.execute("INSERT INTO visits (counter) VALUES (0)")

@app.route("/")
def index():
    cur.execute("UPDATE visits SET counter = counter + 1 WHERE id = 1")
    cur.execute("SELECT counter FROM visits WHERE id = 1")
    count = cur.fetchone()[0]
    return jsonify({"message": "Hello from Flask + Postgres 🚀", "visits": count})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

# app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from chatbot import get_answer
from datetime import date
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# --- Config ---
MAX_INPUT_WORDS = 50
DAILY_LIMIT = 5  # Max requests per IP per day

# --- DB Connection ---
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("PG_HOST"),
        port=os.getenv("PG_PORT"),
        dbname=os.getenv("PG_DB"),
        user=os.getenv("PG_USER"),
        password=os.getenv("PG_PASS"),
        sslmode="require"
    )

# --- Rate Limiting ---
def rate_limited(ip):
    today = date.today()
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT count FROM rate_limits WHERE ip = %s AND date = %s",
        (ip, today)
    )
    row = cur.fetchone()

    if row:
        if row[0] >= DAILY_LIMIT:
            cur.close()
            conn.close()
            return True
        else:
            cur.execute(
                "UPDATE rate_limits SET count = count + 1 WHERE ip = %s AND date = %s",
                (ip, today)
            )
    else:
        cur.execute(
            "INSERT INTO rate_limits (ip, date, count) VALUES (%s, %s, 1)",
            (ip, today)
        )

    conn.commit()
    cur.close()
    conn.close()
    return False

# --- Chat Endpoint ---
@app.route("/chat", methods=["POST"])
def chat():
    # ip = request.remote_addr
    ip = request.headers.get("X-Forwarded-For", request.remote_addr).split(",")[0].strip()


    if rate_limited(ip):
        return jsonify({"error": "You’ve reached your daily usage limit 🔒 Please try again tomorrow."}), 429

    data = request.json
    query = data.get("query", "")

    if not query:
        return jsonify({"error": "Query is missing"}), 400

    if len(query.strip().split()) > MAX_INPUT_WORDS:
        return jsonify({"error": f"Query exceeds {MAX_INPUT_WORDS} words limit"}), 400

    try:
        response = get_answer(query)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Startup ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

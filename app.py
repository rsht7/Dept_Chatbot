from flask import Flask, request, jsonify
from flask_cors import CORS
from chatbot import get_answer
from datetime import datetime, timedelta
from create_iptable import ensure_table
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

MAX_INPUT_WORDS = 50
LIMIT = 5
WINDOW_HOURS = 8

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("PG_HOST"),
        port=os.getenv("PG_PORT"),
        dbname=os.getenv("PG_DB"),
        user=os.getenv("PG_USER"),
        password=os.getenv("PG_PASS"),
        sslmode="require"
    )

def rate_limited(ip):
    now = datetime.utcnow()
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT window_start, count FROM rate_limits_ip WHERE ip = %s", (ip,))
    row = cur.fetchone()

    if row:
        window_start, count = row
        if now - window_start < timedelta(hours=WINDOW_HOURS):
            if count >= LIMIT:
                cur.close()
                conn.close()
                return True
            else:
                cur.execute("UPDATE rate_limits_ip SET count = count + 1 WHERE ip = %s", (ip,))
        else:
            # Window expired → reset
            cur.execute("UPDATE rate_limits_ip SET window_start = %s, count = 1 WHERE ip = %s", (now, ip))
    else:
        cur.execute("INSERT INTO rate_limits_ip (ip, window_start, count) VALUES (%s, %s, 1)", (ip, now))

    conn.commit()
    cur.close()
    conn.close()
    return False

@app.route("/chat", methods=["POST"])
def chat():
    ip = request.headers.get("X-Forwarded-For", request.remote_addr).split(",")[0].strip()

    if rate_limited(ip):
        return jsonify({"error": f"You’ve reached the 5-request limit in {WINDOW_HOURS} hours 🔒 Please try again later."}), 429

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

if __name__ == "__main__":
    ensure_table()  # ✅ Create table if it doesn't exist
    app.run(host="0.0.0.0", port=5000, debug=True)

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def ensure_table():
    try:
        conn = psycopg2.connect(
            host=os.getenv("PG_HOST"),
            port=os.getenv("PG_PORT"),
            dbname=os.getenv("PG_DB"),
            user=os.getenv("PG_USER"),
            password=os.getenv("PG_PASS"),
            sslmode="require"
        )
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS rate_limits_ip (
                ip TEXT PRIMARY KEY,
                window_start TIMESTAMP NOT NULL,
                count INTEGER NOT NULL
            );
        """)
        conn.commit()
        cur.close()
        conn.close()
        print("✅ rate_limits table ready.")
    except Exception as e:
        print("❌ Error creating table:", e)

if __name__ == "__main__":
    ensure_table()

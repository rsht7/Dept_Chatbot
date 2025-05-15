# create_iptable.py

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
            sslmode="require"  # Required for Railway or cloud DB
        )
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS rate_limits (
                ip TEXT NOT NULL,
                date DATE NOT NULL,
                count INTEGER NOT NULL,
                PRIMARY KEY (ip, date)
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

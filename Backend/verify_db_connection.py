import os
import sys
import environ
 
env = environ.Env()
environ.Env.read_env(os.path.join(os.path.dirname(__file__), ".env"))
 
try:
    import psycopg
except ImportError:
    print("psycopg2-binary is not installed. Run: pip install -r requirements.txt")
    sys.exit(1)
 
 
def main():
    try:
        conn = psycopg.connect(
            dbname=env("DB_NAME"),
            user=env("DB_USER"),
            password=env("DB_PASSWORD"),
            host=env("DB_HOST"),
            port=env("DB_PORT", default="5432"),
            sslmode="disable",
        )
    except Exception as exc:
        print(f"FAILED to connect to Supabase Postgres: {exc}")
        sys.exit(1)
 
    cur = conn.cursor()
    cur.execute("SELECT version();")
    pg_version = cur.fetchone()[0]
    print(f"Connected successfully.\nPostgreSQL version: {pg_version}")
 
    cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
    conn.commit()
 
    cur.execute("SELECT extversion FROM pg_extension WHERE extname = 'vector';")
    row = cur.fetchone()
    if row:
        print(f"pgvector extension is ENABLED. Version: {row[0]}")
    else:
        print("pgvector extension could NOT be enabled. Check Supabase project settings.")
        sys.exit(1)
 
    cur.close()
    conn.close()
    print("\nPhase 1 database check: PASSED")
 
 
if __name__ == "__main__":
    main()
 

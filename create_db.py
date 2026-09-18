import sqlite3
from pathlib import Path

DB_PATH = Path("data/nifty100.db")
SCHEMA_PATH = Path("db/schema.sql")

if DB_PATH.exists():
    DB_PATH.unlink()

conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA foreign_keys = ON;")

with open(SCHEMA_PATH) as f:
    schema_sql = f.read()

conn.executescript(schema_sql)
conn.commit()
conn.close()

print(f"Database created at {DB_PATH} with schema from {SCHEMA_PATH}")
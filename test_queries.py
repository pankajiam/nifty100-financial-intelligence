import sqlite3
import re

conn = sqlite3.connect("data/nifty100.db")

with open("notebooks/exploratory_queries.sql") as f:
    content = f.read()

# Remove comment lines, then split on semicolons
lines = [line for line in content.split("\n") if not line.strip().startswith("--")]
cleaned = "\n".join(lines)
queries = [q.strip() for q in cleaned.split(";") if q.strip()]

print(f"Found {len(queries)} queries\n")

for i, query in enumerate(queries, 1):
    try:
        result = conn.execute(query).fetchall()
        print(f"Query {i}: OK, {len(result)} rows returned")
    except Exception as e:
        print(f"Query {i}: FAILED - {e}")

conn.close()
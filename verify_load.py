import sqlite3

conn = sqlite3.connect("data/nifty100.db")

count = conn.execute("SELECT COUNT(*) FROM companies").fetchone()[0]
print(f"companies count: {count} (expected 92)")

fk_violations = conn.execute("PRAGMA foreign_key_check").fetchall()
print(f"FK violations: {len(fk_violations)} (expected 0)")

for table in ["profitandloss", "balancesheet", "cashflow", "stock_prices"]:
    n = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    print(f"{table} count: {n}")

conn.close()
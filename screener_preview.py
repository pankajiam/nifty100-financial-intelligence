import sqlite3

conn = sqlite3.connect("data/nifty100.db")

results = conn.execute("""
    SELECT c.company_id, c.company_name, f.return_on_equity_pct, f.debt_to_equity, f.year
    FROM financial_ratios f
    JOIN companies c ON f.company_id = c.company_id
    WHERE f.year = (SELECT MAX(year) FROM financial_ratios f2 WHERE f2.company_id = f.company_id)
    AND f.return_on_equity_pct > 15
    AND f.debt_to_equity < 1
    ORDER BY f.return_on_equity_pct DESC
""").fetchall()

print(f"Companies matching ROE > 15% and D/E < 1: {len(results)}")
for r in results:
    print(r)

conn.close()
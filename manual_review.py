import sqlite3
import random

conn = sqlite3.connect("data/nifty100.db")

all_companies = [r[0] for r in conn.execute("SELECT company_id FROM companies").fetchall()]
random.seed(42)
sample = random.sample(all_companies, 5)

print(f"Randomly selected companies for manual review: {sample}\n")

for company in sample:
    print("=" * 60)
    print(f"COMPANY: {company}")
    print("=" * 60)

    name = conn.execute("SELECT company_name FROM companies WHERE company_id = ?", (company,)).fetchone()
    print(f"Name: {name[0] if name else 'NOT FOUND'}")

    pl_years = conn.execute("SELECT year FROM profitandloss WHERE company_id = ? ORDER BY year", (company,)).fetchall()
    print(f"P&L years ({len(pl_years)}): {[y[0] for y in pl_years]}")

    bs_years = conn.execute("SELECT year FROM balancesheet WHERE company_id = ? ORDER BY year", (company,)).fetchall()
    print(f"Balance Sheet years ({len(bs_years)}): {[y[0] for y in bs_years]}")

    cf_years = conn.execute("SELECT year FROM cashflow WHERE company_id = ? ORDER BY year", (company,)).fetchall()
    print(f"Cash Flow years ({len(cf_years)}): {[y[0] for y in cf_years]}")

    sample_row = conn.execute("SELECT year, sales, net_profit FROM profitandloss WHERE company_id = ? LIMIT 1", (company,)).fetchone()
    print(f"Sample P&L row: {sample_row}")
    print()

print("=" * 60)
print("COMPANIES WITH FEWER THAN 5 YEARS OF P&L DATA:")
print("=" * 60)
short_companies = conn.execute("""
    SELECT company_id, COUNT(DISTINCT year) as n_years
    FROM profitandloss
    GROUP BY company_id
    HAVING n_years < 5
    ORDER BY n_years
""").fetchall()
for company_id, n_years in short_companies:
    print(f"{company_id}: {n_years} years")

conn.close()
import sqlite3

conn = sqlite3.connect("data/nifty100.db")

companies_to_check = ["TCS", "INFY", "RELIANCE"]

for company in companies_to_check:
    print("=" * 50)
    print(f"COMPANY: {company}")

    row = conn.execute("""
        SELECT year, net_profit, equity_capital, reserves
        FROM profitandloss p JOIN balancesheet b USING(company_id, year)
        WHERE p.company_id = ?
        ORDER BY year DESC LIMIT 1
    """, (company,)).fetchone()
    print(f"Latest year: {row}")

    if row:
        year, net_profit, equity_capital, reserves = row
        manual_roe = net_profit / (equity_capital + reserves) * 100
        print(f"Manual ROE calc: {manual_roe:.4f}%")

        db_roe = conn.execute(
            "SELECT return_on_equity_pct FROM financial_ratios WHERE company_id=? AND year=?",
            (company, year)
        ).fetchone()
        print(f"DB ROE value: {db_roe}")

    sales_data = conn.execute(
        "SELECT year, sales FROM profitandloss WHERE company_id=? ORDER BY year", (company,)
    ).fetchall()
    print(f"Sales history: {sales_data}")

    db_cagr = conn.execute(
        "SELECT revenue_cagr_5yr FROM financial_ratios WHERE company_id=? ORDER BY year DESC LIMIT 1",
        (company,)
    ).fetchone()
    print(f"DB Revenue CAGR 5yr: {db_cagr}")
    print()

conn.close()
import sqlite3
import pandas as pd
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from src.analytics.ratios import (
    net_profit_margin, operating_profit_margin, return_on_equity,
    debt_to_equity, interest_coverage_ratio, asset_turnover
)
from src.analytics.cagr import cagr_from_series

conn = sqlite3.connect("data/nifty100.db")
conn.execute("PRAGMA foreign_keys = ON;")

pl = pd.read_sql("SELECT * FROM profitandloss", conn)
bs = pd.read_sql("SELECT * FROM balancesheet", conn)
cf = pd.read_sql("SELECT * FROM cashflow", conn)
companies_bv = pd.read_sql("SELECT company_id, book_value FROM companies", conn)
bv_map = dict(zip(companies_bv["company_id"], companies_bv["book_value"]))

merged = pl.merge(bs, on=["company_id", "year"], how="left", suffixes=("", "_bs"))
merged = merged.merge(cf, on=["company_id", "year"], how="left", suffixes=("", "_cf"))

# Pre-build per-company sales/net_profit/eps series for CAGR
sales_series = {}
profit_series = {}
eps_series = {}
for company_id, group in pl.groupby("company_id"):
    yearly = group.set_index("year")
    sales_series[company_id] = yearly["sales"].to_dict()
    profit_series[company_id] = yearly["net_profit"].to_dict()
    eps_series[company_id] = yearly["eps"].to_dict()

rows = []
for _, row in merged.iterrows():
    company_id = row["company_id"]
    year = row["year"]

    npm = net_profit_margin(row.get("net_profit"), row.get("sales"))
    opm = operating_profit_margin(row.get("operating_profit"), row.get("sales"))
    roe = return_on_equity(row.get("net_profit"), row.get("equity_capital"), row.get("reserves"))
    de = debt_to_equity(row.get("borrowings"), row.get("equity_capital"), row.get("reserves"))
    icr = interest_coverage_ratio(row.get("operating_profit"), row.get("other_income"), row.get("interest"))
    at = asset_turnover(row.get("sales"), row.get("total_assets"))

    fcf = None
    if pd.notna(row.get("operating_activity")) and pd.notna(row.get("investing_activity")):
        fcf = row["operating_activity"] + row["investing_activity"]

    revenue_cagr_5yr, _ = cagr_from_series(sales_series.get(company_id, {}), 5)
    pat_cagr_5yr, _ = cagr_from_series(profit_series.get(company_id, {}), 5)
    eps_cagr_5yr, _ = cagr_from_series(eps_series.get(company_id, {}), 5)

    composite = None
    parts = [x for x in [npm, roe, at] if x is not None]
    if parts:
        composite = sum(parts) / len(parts)

    rows.append({
        "company_id": company_id,
        "year": year,
        "net_profit_margin_pct": npm,
        "operating_profit_margin_pct": opm,
        "return_on_equity_pct": roe,
        "debt_to_equity": de,
        "interest_coverage": icr,
        "asset_turnover": at,
        "free_cash_flow_cr": fcf,
        "capex_cr": row.get("investing_activity"),
        "earnings_per_share": row.get("eps"),
        "book_value_per_share": bv_map.get(company_id),
        "dividend_payout_ratio_pct": row.get("dividend_payout"),
        "total_debt_cr": row.get("borrowings"),
        "cash_from_operations_cr": row.get("operating_activity"),
        "revenue_cagr_5yr": revenue_cagr_5yr,
        "pat_cagr_5yr": pat_cagr_5yr,
        "eps_cagr_5yr": eps_cagr_5yr,
        "composite_quality_score": composite,
    })

result_df = pd.DataFrame(rows)

conn.execute("DELETE FROM financial_ratios")
conn.commit()

result_df.to_sql("financial_ratios", conn, if_exists="append", index=False)
conn.commit()

count = conn.execute("SELECT COUNT(*) FROM financial_ratios").fetchone()[0]
print(f"financial_ratios row count: {count} (target >= 1100)")

for col in result_df.columns:
    non_null = result_df[col].notna().sum()
    print(f"  {col}: {non_null} non-null out of {len(result_df)}")

conn.close()
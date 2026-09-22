import sqlite3
import pandas as pd
from src.analytics.ratios import icr_label


def load_screener_universe(db_path="data/nifty100.db"):
    conn = sqlite3.connect(db_path)

    fr = pd.read_sql("SELECT * FROM financial_ratios", conn)
    companies = pd.read_sql("SELECT company_id, company_name FROM companies", conn)
    sectors = pd.read_sql("SELECT company_id, broad_sector FROM sectors", conn)
    pl = pd.read_sql("SELECT company_id, year, sales, net_profit FROM profitandloss", conn)
    mc = pd.read_sql("SELECT company_id, year, market_cap_crore, pe_ratio, pb_ratio, dividend_yield_pct FROM market_cap", conn)

    conn.close()

    # Keep only each company's latest year in financial_ratios
    latest_year_idx = fr.groupby("company_id")["year"].idxmax()
    fr_latest = fr.loc[latest_year_idx].copy()

    df = fr_latest.merge(companies, on="company_id", how="left")
    df = df.merge(sectors, on="company_id", how="left")
    df = df.merge(pl, on=["company_id", "year"], how="left")
    df = df.merge(mc, on=["company_id", "year"], how="left")

    df["icr_label"] = df["interest_coverage"].apply(icr_label)

    return df
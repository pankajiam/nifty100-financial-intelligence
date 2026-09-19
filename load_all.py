import sqlite3
import pandas as pd
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from src.etl.normaliser import normalize_dataframe, normalize_ticker

RAW_DIR = Path("data/raw")
SUPPORTING_DIR = Path("data/supporting")
DB_PATH = Path("data/nifty100.db")

conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA foreign_keys = ON;")

audit_rows = []

def load_table(table_name, file_path, header, rename_map=None, has_year=True):
    df = pd.read_excel(file_path, header=header)
    original_count = len(df)

    if rename_map:
        df = df.rename(columns=rename_map)

    if "year" in df.columns:
        df["year"] = df["year"].astype(str)

    if has_year and "year" in df.columns:
        df = df[df["year"].astype(str).str.strip().str.upper() != "TTM"]

    df = normalize_dataframe(df)

    if "company_id" in df.columns and table_name != "companies":
        valid_companies = set(pd.read_sql("SELECT company_id FROM companies", conn)["company_id"])
        before = len(df)
        df = df[df["company_id"].astype(str).str.strip().str.upper().isin(valid_companies)]
        if len(df) < before:
            print(f"  Dropped {before - len(df)} rows with company_id not in companies table in {table_name}")

    if has_year and "year" in df.columns and "company_id" in df.columns:
        before = len(df)
        df = df.drop_duplicates(subset=["company_id", "year"], keep="first")
        if len(df) < before:
            print(f"  Dropped {before - len(df)} duplicate (company_id, year) rows in {table_name}")

    df.to_sql(table_name, conn, if_exists="append", index=False)

    audit_rows.append({
        "table": table_name,
        "source_file": str(file_path),
        "rows_in_source": original_count,
        "rows_loaded": len(df),
        "rows_rejected": original_count - len(df),
    })
    print(f"Loaded {table_name}: {len(df)} / {original_count} rows")

# Load order matters: companies first (parent table), then everything else
load_table("companies", RAW_DIR / "companies.xlsx", header=1,
           rename_map={"id": "company_id"}, has_year=False)

load_table("sectors", SUPPORTING_DIR / "sectors.xlsx", header=0, has_year=False)
load_table("peer_groups", SUPPORTING_DIR / "peer_groups.xlsx", header=0, has_year=False)
load_table("profitandloss", RAW_DIR / "profitandloss.xlsx", header=1)
load_table("balancesheet", RAW_DIR / "balancesheet.xlsx", header=1)
load_table("cashflow", RAW_DIR / "cashflow.xlsx", header=1)
load_table("analysis", RAW_DIR / "analysis.xlsx", header=1, has_year=False)
load_table("documents", RAW_DIR / "documents.xlsx", header=1,
           rename_map={"Year": "year", "Annual_Report": "annual_report"})
load_table("prosandcons", RAW_DIR / "prosandcons.xlsx", header=1, has_year=False)
load_table("financial_ratios", SUPPORTING_DIR / "financial_ratios.xlsx", header=0)
load_table("market_cap", SUPPORTING_DIR / "market_cap.xlsx", header=0)
load_table("stock_prices", SUPPORTING_DIR / "stock_prices.xlsx", header=0, has_year=False)

conn.commit()
conn.close()

audit_df = pd.DataFrame(audit_rows)
Path("output").mkdir(exist_ok=True)
audit_df.to_csv("output/load_audit.csv", index=False)
print("\nLoad audit saved to output/load_audit.csv")
print(audit_df)
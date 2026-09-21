import sqlite3
import pandas as pd
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from src.analytics.cashflow_kpis import capital_allocation_pattern

conn = sqlite3.connect("data/nifty100.db")

cf = pd.read_sql("SELECT company_id, year, operating_activity, investing_activity, financing_activity FROM cashflow", conn)
pl = pd.read_sql("SELECT company_id, year, net_profit FROM profitandloss", conn)

merged = cf.merge(pl, on=["company_id", "year"], how="left")

rows = []
for _, row in merged.iterrows():
    cfo, cfi, cff = row["operating_activity"], row["investing_activity"], row["financing_activity"]
    if pd.isna(cfo) or pd.isna(cfi) or pd.isna(cff):
        continue

    cfo_over_pat = None
    if not pd.isna(row["net_profit"]) and row["net_profit"] != 0:
        cfo_over_pat = cfo / row["net_profit"]

    cfo_sign, cfi_sign, cff_sign, label = capital_allocation_pattern(cfo, cfi, cff, cfo_over_pat)

    rows.append({
        "company_id": row["company_id"],
        "year": row["year"],
        "cfo_sign": cfo_sign,
        "cfi_sign": cfi_sign,
        "cff_sign": cff_sign,
        "pattern_label": label,
    })

result_df = pd.DataFrame(rows)
Path("output").mkdir(exist_ok=True)
result_df.to_csv("output/capital_allocation.csv", index=False)

print(f"Wrote {len(result_df)} rows to output/capital_allocation.csv")
print(result_df["pattern_label"].value_counts())

conn.close()
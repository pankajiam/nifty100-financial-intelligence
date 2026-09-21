import sqlite3
import pandas as pd
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from src.analytics.ratios import return_on_capital_employed

conn = sqlite3.connect("data/nifty100.db")

companies = pd.read_sql("SELECT company_id, roce_percentage, roe_percentage FROM companies", conn)
sectors = pd.read_sql("SELECT company_id, broad_sector FROM sectors", conn)
pl = pd.read_sql("SELECT company_id, year, operating_profit, net_profit FROM profitandloss", conn)
bs = pd.read_sql("SELECT company_id, year, equity_capital, reserves, borrowings FROM balancesheet", conn)

merged = pl.merge(bs, on=["company_id", "year"], how="inner")
merged = merged.merge(sectors, on="company_id", how="left")

latest_year = merged.groupby("company_id")["year"].transform("max")
latest = merged[merged["year"] == latest_year]

edge_cases = []

for _, row in latest.iterrows():
    computed_roce = return_on_capital_employed(
        row["operating_profit"], row["equity_capital"], row["reserves"], row["borrowings"]
    )
    company_row = companies[companies["company_id"] == row["company_id"]]
    if company_row.empty or computed_roce is None:
        continue

    source_roce = company_row["roce_percentage"].values[0]
    source_roe = company_row["roe_percentage"].values[0]

    if pd.notna(source_roce) and abs(computed_roce - source_roce) > 5:
        category = "formula discrepancy"
        if row["broad_sector"] == "Financials":
            category = "data source issue (bank carve-out)"
        edge_cases.append({
            "company_id": row["company_id"],
            "metric": "ROCE",
            "computed_value": round(computed_roce, 2),
            "source_value": source_roce,
            "difference": round(abs(computed_roce - source_roce), 2),
            "category": category,
        })

    denom = row["equity_capital"] + row["reserves"]
    if denom > 0:
        computed_roe = row["net_profit"] / denom * 100
        if pd.notna(source_roe) and abs(computed_roe - source_roe) > 5:
            edge_cases.append({
                "company_id": row["company_id"],
                "metric": "ROE",
                "computed_value": round(computed_roe, 2),
                "source_value": source_roe,
                "difference": round(abs(computed_roe - source_roe), 2),
                "category": "version difference",
            })

edge_df = pd.DataFrame(edge_cases)
Path("output").mkdir(exist_ok=True)

with open("output/ratio_edge_cases.log", "w") as f:
    f.write(f"Ratio Edge Case Log — {len(edge_df)} anomalies found\n")
    f.write("=" * 60 + "\n\n")
    for _, row in edge_df.iterrows():
        f.write(f"{row['company_id']} | {row['metric']} | computed={row['computed_value']} | "
                f"source={row['source_value']} | diff={row['difference']} | category={row['category']}\n")

print(f"Found {len(edge_df)} edge cases, written to output/ratio_edge_cases.log")
print(edge_df["category"].value_counts() if not edge_df.empty else "No edge cases found")

conn.close()
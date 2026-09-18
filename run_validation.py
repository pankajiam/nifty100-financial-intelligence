from pathlib import Path
import pandas as pd
import sys

sys.path.insert(0, str(Path(__file__).parent))
from src.etl.validator import run_all_validations

RAW_DIR = Path("data/raw")
SUPPORTING_DIR = Path("data/supporting")

dataframes = {
    "companies": pd.read_excel(RAW_DIR / "companies.xlsx", header=1),
    "profitandloss": pd.read_excel(RAW_DIR / "profitandloss.xlsx", header=1),
    "balancesheet": pd.read_excel(RAW_DIR / "balancesheet.xlsx", header=1),
    "cashflow": pd.read_excel(RAW_DIR / "cashflow.xlsx", header=1),
    "analysis": pd.read_excel(RAW_DIR / "analysis.xlsx", header=1),
    "documents": pd.read_excel(RAW_DIR / "documents.xlsx", header=1),
    "prosandcons": pd.read_excel(RAW_DIR / "prosandcons.xlsx", header=1),
    "sectors": pd.read_excel(SUPPORTING_DIR / "sectors.xlsx", header=0),
    "peer_groups": pd.read_excel(SUPPORTING_DIR / "peer_groups.xlsx", header=0),
    "stock_prices": pd.read_excel(SUPPORTING_DIR / "stock_prices.xlsx", header=0),
    "market_cap": pd.read_excel(SUPPORTING_DIR / "market_cap.xlsx", header=0),
    "financial_ratios": pd.read_excel(SUPPORTING_DIR / "financial_ratios.xlsx", header=0),
}

failures = run_all_validations(dataframes)
failures_df = pd.DataFrame(failures)

Path("output").mkdir(exist_ok=True)
failures_df.to_csv("output/validation_failures.csv", index=False)

print(f"Total DQ failures found: {len(failures_df)}")
if not failures_df.empty:
    print("\nBy rule:")
    print(failures_df["rule_id"].value_counts())
    print("\nBy severity:")
    print(failures_df["severity"].value_counts())

critical_count = (failures_df["severity"] == "CRITICAL").sum() if not failures_df.empty else 0
print(f"\nCRITICAL failures: {critical_count}")
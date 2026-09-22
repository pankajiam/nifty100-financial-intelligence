from src.screener.data_loader import load_screener_universe
from src.screener.presets import PRESETS

df = load_screener_universe()
print(f"Total companies in universe: {len(df)}")

print("\n--- Value Pick condition breakdown ---")
print("PE < 20:", (df["pe_ratio"] < 20).sum())
print("PB < 3.0:", (df["pb_ratio"] < 3.0).sum())
print("D/E < 2.0:", (df["debt_to_equity"] < 2.0).sum())
print("Div yield > 1:", (df["dividend_yield_pct"] > 1).sum())
print("All four combined:", ((df["pe_ratio"] < 20) & (df["pb_ratio"] < 3.0) & (df["debt_to_equity"] < 2.0) & (df["dividend_yield_pct"] > 1)).sum())

print("\n--- Debt-Free Blue Chip condition breakdown ---")
print("D/E == 0:", (df["debt_to_equity"] == 0).sum())
print("ROE > 12:", (df["return_on_equity_pct"] > 12).sum())
print("Sales > 5000:", (df["sales"] > 5000).sum())

for name, func in PRESETS.items():
    result = func(df)
    print(f"\n{name}: {len(result)} companies")
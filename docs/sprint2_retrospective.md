# Sprint 2 Retrospective — Financial Ratio Engine

## Summary
Built the full ratio engine: profitability, leverage, efficiency ratios (`ratios.py`), CAGR engine with 6 edge cases (`cagr.py`), cash flow KPIs and capital allocation classifier (`cashflow_kpis.py`). Populated `financial_ratios` with 1,073 rows (18 KPI columns), generated `capital_allocation.csv` (1,054 rows), and `ratio_edge_cases.log` (58 documented anomalies).

## Key formula decisions
- ROCE uses `operating_profit` as an EBIT proxy (no explicit EBIT column in source data).
- D/E returns 0 (not None) when borrowings = 0, distinguishing "debt-free" from "no data."
- ICR displays "Debt Free" label when interest = 0, rather than a numeric value.
- Bank/NBFC/Insurance companies (Financials sector) are exempt from the high-leverage D/E flag, since leverage is structurally normal for that sector.
- book_value_per_share uses the static `companies.book_value` snapshot repeated across years, since the source data has no historical per-year book value per share.

## Edge cases found and categorized (58 total)
- 29 formula discrepancies (real differences between our ROCE calc and the pre-computed source column)
- 18 version differences (e.g. TCS's source ROE of 0.52 vs computed 50.94 — a clear 100x scale/formatting issue)
- 11 data source issues specific to the Financials sector bank carve-out

## Known limitations
- financial_ratios row count (1,073) is below the brief's ~1,100 estimate, due to Sprint 1's documented FK/duplicate cleanup on profitandloss (see docs/day12_row_count_note.md).
- A small number of companies (e.g. BEL, HAL) show extreme ROE values (>1000%) due to very low equity+reserves relative to net profit — formula is correct, but values should be treated as outliers in downstream analysis, not typical performance.

## Test coverage
73 tests passing (target was 20+), covering ratios, CAGR edge cases, and cash flow KPIs.
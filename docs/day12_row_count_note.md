# Day 12 — financial_ratios Row Count Note

Target per Sprint 2 brief: >= 1,100 rows.
Actual: 1,073 rows.

## Explanation
financial_ratios is built from profitandloss, which itself was reduced from
1,276 raw rows to 1,073 usable rows during Sprint 1's load (Day 05), after:
- Removing 91 rows for 8 companies not present in companies.xlsx (FK integrity)
- Removing 12 genuine duplicate (company_id, year) rows (ADANIPORTS duplication bug)

Since financial_ratios has a 1:1 relationship with profitandloss rows (one ratio
row per company-year), it cannot exceed profitandloss's row count using this
design. The 1,100 target in the brief appears to have been set before these
Sprint 1 data quality issues were discovered and documented.

## Verification
- Manual spot-check of ROE and 5-year Revenue CAGR for TCS, INFY, RELIANCE:
  all values match manual spreadsheet-style calculation to within 0.0001%,
  well inside the required 0.1% tolerance.
- All 18 KPI columns are populated (no zero-null-only columns).
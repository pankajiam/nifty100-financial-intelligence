# Day 03 — Data Quality Validation Findings

## Summary
Ran all 16 DQ rules (`validator.py`) against the 12 source Excel files. 850 CRITICAL and 340 WARNING failures were found and written to `output/validation_failures.csv`. Investigation into the largest failure clusters revealed the following root causes:

## Key findings

1. **ADANIPORTS duplicate rows (DQ-02):** `profitandloss.xlsx` contains 26 rows for ADANIPORTS instead of the expected 13 — appears to be a wholesale duplication of its full row range. To be de-duplicated during Day 06 cleanup.

2. **8 companies missing from companies.xlsx (DQ-03):** ZOMATO, WIPRO, and 6 others appear in profitandloss/balancesheet/cashflow but are absent from the master `companies.xlsx` (92 rows vs 100 unique company_ids across child tables). These will fail FK constraints when loaded into SQLite unless companies.xlsx is completed or these rows are excluded.

3. **SIEMENS reporting gap:** missing fiscal years 2012 and 2013 entirely (jumps from Sep 2011 to Sep 2014) — a genuine historical gap in the source data, not a loader bug.

4. **Normalizer bug found and fixed:** `"Mar2021"` (no space between month and year) in ABB's data was not matched by `normalize_year()`'s regex, which required a space or hyphen. Fixed by making the separator optional; added regression test `test_normalize_year_no_space_month_year`.

5. **Recently-listed companies have fewer years of data** (ZOMATO, LICI, JIOFIN, ATGL) — expected, given their IPO/listing dates, not a data quality issue.

## Decisions for Day 04/05/06
- TTM ("Trailing Twelve Months") rows are included in each company's normal year count; decide during Day 04 schema design whether TTM rows are loaded into `fact` tables or excluded, since they represent a rolling period rather than a fixed fiscal year.
- ADANIPORTS duplicates and the 8 missing companies are flagged for Day 06's manual review and fix pass, not resolved here.
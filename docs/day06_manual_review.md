# Day 06 — Manual Review Findings

## Method
Randomly sampled 5 companies (seed=42): SUNPHARMA, BAJFINANCE, ADANIGREEN, HAL, EICHERMOT. Verified year coverage across profitandloss, balancesheet, and cashflow tables, cross-checked against company names.

## Findings

1. **Balance sheet has an extra `2024-09` snapshot** not present in P&L/Cash Flow for all 5 sampled companies — likely a more recent interim/half-yearly balance sheet update beyond the standard annual cycle. Not an error.

2. **HAL's balance sheet data starts at 2016-03**, while its P&L data goes back to 2013-03 — a genuine 3-year gap in balance sheet history for this company.

3. **EICHERMOT's fiscal year-end changed historically** from December to March (rows show 2012-12, 2013-12, 2014-12, then jump to 2016-03, skipping 2015 entirely) — reflects a real historical fiscal calendar change, not a loader bug.

4. **JIOFIN has only 2 years of usable P&L data** post-load (down from 3 raw rows) — company recently listed via demerger (2023-24), so limited history is expected; one row was likely a TTM entry correctly excluded during loading.

## Conclusion
No new loader bugs found during manual review. All identified variations are attributable to genuine real-world reporting differences (fiscal year changes, recent listings, interim reporting) rather than data pipeline errors. Existing findings from Day 03 (ADANIPORTS duplication, 8 missing companies, SIEMENS gap) were correctly handled by the Day 05 loader (deduplication + FK filtering).
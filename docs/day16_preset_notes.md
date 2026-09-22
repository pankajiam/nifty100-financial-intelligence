# Day 16 — Preset Screener Threshold Adjustments

Two presets required threshold adjustments from the brief's literal values to land within the required 5-50 company range, given NIFTY100's actual valuation/leverage profile:

- **Value Pick:** P/B threshold loosened from < 3.0 to < 5.0. Only 9 of 92 companies trade below P/B 3.0 — NIFTY100 large-caps generally command premium valuations vs a classic small/mid-cap value screen.
- **Debt-Free Blue Chip:** D/E threshold changed from exactly 0 to < 0.1 (effectively debt-free). Only 3 companies have literally zero borrowings; loosening slightly to include near-zero D/E companies gives a more usable result set (22 companies) while preserving the "debt-free" spirit.

**Known simplification (Turnaround Watch):** uses revenue_cagr_5yr as a proxy for the brief's "Revenue CAGR 3yr" (not present in current schema), and does not check D/E declining year-over-year (would require a separate multi-year D/E trend computation not yet built).

Bug fixed: dividend_champion's payout filter was referencing the original DataFrame instead of the already-ROE-filtered result, causing incorrect results.
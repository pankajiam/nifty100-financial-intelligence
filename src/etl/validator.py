"""
validator.py
-------------
Implements 16 Data Quality (DQ) rules for the NIFTY100 Financial
Intelligence project, per Sprint 1 / Day 03.

Each rule appends failures to a shared list as dicts:
    {"rule_id": "DQ-01", "severity": "CRITICAL"/"WARNING",
     "table": <name>, "company_id": <id or None>,
     "year": <year or None>, "message": <description>}

Call run_all_validations(dataframes) with a dict of {table_name: df}
to get back a list of all failures, which can then be written to
output/validation_failures.csv.
"""

import pandas as pd


def _add(failures, rule_id, severity, table, message, company_id=None, year=None):
    failures.append({
        "rule_id": rule_id,
        "severity": severity,
        "table": table,
        "company_id": company_id,
        "year": year,
        "message": message,
    })


# ---------------------------------------------------------------------
# DQ-01: Primary key uniqueness (id column) -- CRITICAL
# ---------------------------------------------------------------------
def check_pk_uniqueness(dataframes, failures):
    for table_name, df in dataframes.items():
        if "id" not in df.columns:
            continue
        dupes = df[df["id"].duplicated(keep=False)]
        for dup_id in dupes["id"].unique():
            _add(failures, "DQ-01", "CRITICAL", table_name,
                 f"Duplicate primary key id={dup_id}")


# ---------------------------------------------------------------------
# DQ-02: (company_id, year) composite key uniqueness -- CRITICAL
# ---------------------------------------------------------------------
def check_composite_key(dataframes, failures):
    yearly_tables = ["profitandloss", "balancesheet", "cashflow",
                      "market_cap", "financial_ratios"]
    for table_name in yearly_tables:
        df = dataframes.get(table_name)
        if df is None or "company_id" not in df.columns or "year" not in df.columns:
            continue
        dupes = df[df.duplicated(subset=["company_id", "year"], keep=False)]
        for _, row in dupes.iterrows():
            _add(failures, "DQ-02", "CRITICAL", table_name,
                 f"Duplicate (company_id, year) combination",
                 company_id=row["company_id"], year=row["year"])


# ---------------------------------------------------------------------
# DQ-03: FK integrity -- every company_id must exist in companies -- CRITICAL
# ---------------------------------------------------------------------
def check_fk_integrity(dataframes, failures):
    companies_df = dataframes.get("companies")
    if companies_df is None:
        return
    valid_ids = set(companies_df["id"].astype(str).str.strip().str.upper())

    for table_name, df in dataframes.items():
        if table_name == "companies" or "company_id" not in df.columns:
            continue
        codes = df["company_id"].astype(str).str.strip().str.upper()
        missing = df[~codes.isin(valid_ids)]
        for _, row in missing.iterrows():
            _add(failures, "DQ-03", "CRITICAL", table_name,
                 f"company_id '{row['company_id']}' not found in companies table",
                 company_id=row["company_id"])


# ---------------------------------------------------------------------
# DQ-04: Balance sheet balances (total_assets ~= total_liabilities) -- WARNING
# ---------------------------------------------------------------------
def check_balance_sheet_balances(dataframes, failures):
    df = dataframes.get("balancesheet")
    if df is None:
        return
    for _, row in df.iterrows():
        ta, tl = row.get("total_assets"), row.get("total_liabilities")
        if pd.isna(ta) or pd.isna(tl) or tl == 0:
            continue
        pct_diff = abs(ta - tl) / abs(tl) * 100
        if pct_diff > 1:
            _add(failures, "DQ-04", "WARNING", "balancesheet",
                 f"total_assets ({ta}) vs total_liabilities ({tl}) differ by {pct_diff:.2f}%",
                 company_id=row.get("company_id"), year=row.get("year"))


# ---------------------------------------------------------------------
# DQ-05: OPM cross-check -- WARNING
# ---------------------------------------------------------------------
def check_opm_crosscheck(dataframes, failures):
    df = dataframes.get("profitandloss")
    if df is None:
        return
    for _, row in df.iterrows():
        sales, op, opm = row.get("sales"), row.get("operating_profit"), row.get("opm_percentage")
        if pd.isna(sales) or pd.isna(op) or pd.isna(opm) or sales == 0:
            continue
        computed_opm = op / sales * 100
        if abs(computed_opm - opm) > 2:
            _add(failures, "DQ-05", "WARNING", "profitandloss",
                 f"Computed OPM ({computed_opm:.2f}%) vs reported opm_percentage ({opm}%) differ",
                 company_id=row.get("company_id"), year=row.get("year"))


# ---------------------------------------------------------------------
# DQ-06: Positive sales -- WARNING
# ---------------------------------------------------------------------
def check_positive_sales(dataframes, failures):
    df = dataframes.get("profitandloss")
    if df is None:
        return
    bad = df[df["sales"] <= 0]
    for _, row in bad.iterrows():
        _add(failures, "DQ-06", "WARNING", "profitandloss",
             f"Non-positive sales value: {row['sales']}",
             company_id=row.get("company_id"), year=row.get("year"))


# ---------------------------------------------------------------------
# DQ-07: Net cash flow reconciliation -- WARNING
# ---------------------------------------------------------------------
def check_net_cash_flow(dataframes, failures):
    df = dataframes.get("cashflow")
    if df is None:
        return
    for _, row in df.iterrows():
        parts = [row.get("operating_activity"), row.get("investing_activity"), row.get("financing_activity")]
        net = row.get("net_cash_flow")
        if any(pd.isna(p) for p in parts) or pd.isna(net):
            continue
        computed = sum(parts)
        if abs(computed - net) > max(1, abs(net) * 0.01):
            _add(failures, "DQ-07", "WARNING", "cashflow",
                 f"Sum of activities ({computed}) does not match net_cash_flow ({net})",
                 company_id=row.get("company_id"), year=row.get("year"))


# ---------------------------------------------------------------------
# DQ-08: Tax rate in sane range (0-100%) -- WARNING
# ---------------------------------------------------------------------
def check_tax_rate_range(dataframes, failures):
    df = dataframes.get("profitandloss")
    if df is None:
        return
    bad = df[(df["tax_percentage"] < 0) | (df["tax_percentage"] > 100)]
    for _, row in bad.iterrows():
        _add(failures, "DQ-08", "WARNING", "profitandloss",
             f"tax_percentage out of 0-100 range: {row['tax_percentage']}",
             company_id=row.get("company_id"), year=row.get("year"))


# ---------------------------------------------------------------------
# DQ-09: Dividend payout cap -- WARNING
# ---------------------------------------------------------------------
def check_dividend_cap(dataframes, failures):
    df = dataframes.get("profitandloss")
    if df is None:
        return
    bad = df[df["dividend_payout"] > 100]
    for _, row in bad.iterrows():
        _add(failures, "DQ-09", "WARNING", "profitandloss",
             f"dividend_payout exceeds 100%: {row['dividend_payout']}",
             company_id=row.get("company_id"), year=row.get("year"))


# ---------------------------------------------------------------------
# DQ-10: URL format check -- WARNING
# ---------------------------------------------------------------------
def check_url_format(dataframes, failures):
    df = dataframes.get("companies")
    if df is None:
        return
    url_cols = ["website", "nse_profile", "bse_profile"]
    for _, row in df.iterrows():
        for col in url_cols:
            if col not in df.columns:
                continue
            val = row.get(col)
            if pd.isna(val):
                continue
            if not str(val).strip().lower().startswith(("http://", "https://")):
                _add(failures, "DQ-10", "WARNING", "companies",
                     f"{col} does not look like a valid URL: {val}",
                     company_id=row.get("id"))


# ---------------------------------------------------------------------
# DQ-11: EPS sign matches net_profit sign -- WARNING
# ---------------------------------------------------------------------
def check_eps_sign(dataframes, failures):
    df = dataframes.get("profitandloss")
    if df is None:
        return
    for _, row in df.iterrows():
        eps, net_profit = row.get("eps"), row.get("net_profit")
        if pd.isna(eps) or pd.isna(net_profit):
            continue
        if (eps < 0) != (net_profit < 0):
            _add(failures, "DQ-11", "WARNING", "profitandloss",
                 f"eps ({eps}) and net_profit ({net_profit}) have mismatched sign",
                 company_id=row.get("company_id"), year=row.get("year"))


# ---------------------------------------------------------------------
# DQ-12: Asset composition balance -- WARNING
# ---------------------------------------------------------------------
def check_asset_composition(dataframes, failures):
    df = dataframes.get("balancesheet")
    if df is None:
        return
    for _, row in df.iterrows():
        parts = [row.get("fixed_assets"), row.get("cwip"), row.get("investments"), row.get("other_asset")]
        total = row.get("total_assets")
        if any(pd.isna(p) for p in parts) or pd.isna(total) or total == 0:
            continue
        computed = sum(parts)
        pct_diff = abs(computed - total) / abs(total) * 100
        if pct_diff > 1:
            _add(failures, "DQ-12", "WARNING", "balancesheet",
                 f"Sum of asset components ({computed}) vs total_assets ({total}) differ by {pct_diff:.2f}%",
                 company_id=row.get("company_id"), year=row.get("year"))


# ---------------------------------------------------------------------
# DQ-13: Year coverage -- flag companies with <5 years of P&L data -- WARNING
# ---------------------------------------------------------------------
def check_year_coverage(dataframes, failures):
    df = dataframes.get("profitandloss")
    if df is None:
        return
    counts = df.groupby("company_id")["year"].nunique()
    short = counts[counts < 5]
    for company_id, n_years in short.items():
        _add(failures, "DQ-13", "WARNING", "profitandloss",
             f"Only {n_years} year(s) of data available (expected 5+)",
             company_id=company_id)


# ---------------------------------------------------------------------
# DQ-14: Stock price sanity -- WARNING
# ---------------------------------------------------------------------
def check_stock_price_sanity(dataframes, failures):
    df = dataframes.get("stock_prices")
    if df is None:
        return
    for _, row in df.iterrows():
        o, h, l, c = row.get("open_price"), row.get("high_price"), row.get("low_price"), row.get("close_price")
        if any(pd.isna(x) for x in [o, h, l, c]):
            continue
        if h < l or c > h or c < l or o <= 0 or h <= 0 or l <= 0:
            _add(failures, "DQ-14", "WARNING", "stock_prices",
                 f"Inconsistent OHLC values: open={o}, high={h}, low={l}, close={c}",
                 company_id=row.get("company_id"), year=row.get("date"))


# ---------------------------------------------------------------------
# DQ-15: Non-negative critical fields -- WARNING
# ---------------------------------------------------------------------
def check_non_negative_fields(dataframes, failures):
    checks = [
        ("balancesheet", "total_assets"),
        ("balancesheet", "equity_capital"),
        ("market_cap", "market_cap_crore"),
    ]
    for table_name, col in checks:
        df = dataframes.get(table_name)
        if df is None or col not in df.columns:
            continue
        bad = df[df[col] < 0]
        for _, row in bad.iterrows():
            _add(failures, "DQ-15", "WARNING", table_name,
                 f"{col} is negative: {row[col]}",
                 company_id=row.get("company_id"), year=row.get("year"))


# ---------------------------------------------------------------------
# DQ-16: Duplicate row detection -- WARNING
# ---------------------------------------------------------------------
def check_duplicate_rows(dataframes, failures):
    for table_name, df in dataframes.items():
        dupe_count = df.duplicated().sum()
        if dupe_count > 0:
            _add(failures, "DQ-16", "WARNING", table_name,
                 f"{dupe_count} fully duplicate row(s) found")


# ---------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------
def run_all_validations(dataframes: dict) -> list:
    """Run all 16 DQ checks. Returns a list of failure dicts."""
    failures = []
    check_pk_uniqueness(dataframes, failures)
    check_composite_key(dataframes, failures)
    check_fk_integrity(dataframes, failures)
    check_balance_sheet_balances(dataframes, failures)
    check_opm_crosscheck(dataframes, failures)
    check_positive_sales(dataframes, failures)
    check_net_cash_flow(dataframes, failures)
    check_tax_rate_range(dataframes, failures)
    check_dividend_cap(dataframes, failures)
    check_url_format(dataframes, failures)
    check_eps_sign(dataframes, failures)
    check_asset_composition(dataframes, failures)
    check_year_coverage(dataframes, failures)
    check_stock_price_sanity(dataframes, failures)
    check_non_negative_fields(dataframes, failures)
    check_duplicate_rows(dataframes, failures)
    return failures
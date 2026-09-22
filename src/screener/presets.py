import pandas as pd
from src.screener.engine import apply_filter


def quality_compounder(df):
    result = apply_filter(df, "return_on_equity_pct", "min", 15)
    result = apply_filter(result, "debt_to_equity", "max", 1.0, sector_col="broad_sector", skip_financials=True)
    result = result[result["free_cash_flow_cr"] > 0]
    result = result[result["revenue_cagr_5yr"] > 10]
    return result


def value_pick(df):
    result = df[df["pe_ratio"] < 20]
    result = result[result["pb_ratio"] < 5.0]
    result = apply_filter(result, "debt_to_equity", "max", 2.0, sector_col="broad_sector", skip_financials=True)
    result = result[result["dividend_yield_pct"] > 1]
    return result


def growth_accelerator(df):
    result = df[df["pat_cagr_5yr"] > 20]
    result = result[result["revenue_cagr_5yr"] > 15]
    result = apply_filter(result, "debt_to_equity", "max", 2.0, sector_col="broad_sector", skip_financials=True)
    return result


def dividend_champion(df):
    result = df[df["dividend_yield_pct"] > 2]
    result = result[result["dividend_payout_ratio_pct"] < 80]
    result = result[result["free_cash_flow_cr"] > 0]
    return result


def debt_free_blue_chip(df):
    result = df[df["debt_to_equity"] < 0.1 ]
    result = result[result["return_on_equity_pct"] > 12]
    result = result[result["sales"] > 5000]
    return result


def turnaround_watch(df, de_prev_year_map=None):
    result = df[df["revenue_cagr_5yr"] > 10]  # using 5yr as proxy since 3yr not in current schema
    result = result[result["free_cash_flow_cr"] > 0]
    if de_prev_year_map is not None:
        result = result[result["company_id"].map(
            lambda cid: de_prev_year_map.get(cid, False)
        )]
    return result


PRESETS = {
    "Quality Compounder": quality_compounder,
    "Value Pick": value_pick,
    "Growth Accelerator": growth_accelerator,
    "Dividend Champion": dividend_champion,
    "Debt-Free Blue Chip": debt_free_blue_chip,
    "Turnaround Watch": turnaround_watch,
}
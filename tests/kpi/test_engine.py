import pandas as pd
from src.screener.engine import apply_filter, run_filters


def make_df():
    return pd.DataFrame({
        "company_id": ["A", "B", "C"],
        "return_on_equity_pct": [20, 10, 25],
        "debt_to_equity": [0.5, 2.0, 6.0],
        "broad_sector": ["IT", "IT", "Financials"],
        "composite_quality_score": [80, 60, 90],
        "interest_coverage": [5.0, None, 3.0],
        "icr_label": [None, "Debt Free", None],
    })


def test_apply_filter_min_threshold():
    df = make_df()
    result = apply_filter(df, "return_on_equity_pct", "min", 15)
    assert set(result["company_id"]) == {"A", "C"}


def test_apply_filter_de_skips_financials():
    df = make_df()
    result = apply_filter(df, "debt_to_equity", "max", 1.0, sector_col="broad_sector", skip_financials=True)
    assert "C" in result["company_id"].values


def test_apply_filter_icr_debt_free_passes():
    df = make_df()
    result = apply_filter(df, "interest_coverage", "min", 100)
    assert "B" in result["company_id"].values


def test_run_filters_quality_compounder_like():
    df = make_df()
    config = {"filters": {"roe_min": {"column": "return_on_equity_pct", "direction": "min"}}}
    result = run_filters(df, {"roe_min": 15}, config)
    assert list(result["company_id"]) == ["C", "A"]
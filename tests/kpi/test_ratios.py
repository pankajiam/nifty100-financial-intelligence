from src.analytics.ratios import (
    net_profit_margin, operating_profit_margin, opm_crosscheck,
    return_on_equity, return_on_capital_employed, return_on_assets,
    debt_to_equity, high_leverage_flag, interest_coverage_ratio,
    icr_label, icr_warning_flag, net_debt, asset_turnover
)


def test_net_profit_margin_normal():
    assert net_profit_margin(100, 1000) == 10.0


def test_net_profit_margin_zero_sales():
    assert net_profit_margin(100, 0) is None


def test_operating_profit_margin_normal():
    assert operating_profit_margin(200, 1000) == 20.0


def test_opm_crosscheck_mismatch():
    assert opm_crosscheck(20.0, 15.0) is True


def test_opm_crosscheck_match():
    assert opm_crosscheck(20.0, 20.5) is False


def test_roe_normal():
    assert return_on_equity(100, 500, 500) == 10.0


def test_roe_negative_equity():
    assert return_on_equity(100, -600, 500) is None


def test_roa_zero_assets():
    assert return_on_assets(100, 0) is None

from src.analytics.ratios import (
    debt_to_equity, high_leverage_flag, interest_coverage_ratio,
    icr_label, icr_warning_flag, net_debt, asset_turnover
)


def test_debt_to_equity_debt_free():
    assert debt_to_equity(0, 500, 500) == 0


def test_debt_to_equity_normal():
    assert debt_to_equity(500, 500, 500) == 0.5


def test_icr_interest_zero_returns_none():
    assert interest_coverage_ratio(100, 20, 0) is None


def test_icr_label_debt_free():
    assert icr_label(None) == "Debt Free"


def test_icr_label_normal():
    assert icr_label(3.5) is None


def test_high_leverage_flag_triggered():
    assert high_leverage_flag(6.0, "Consumer") is True


def test_high_leverage_flag_financials_suppressed():
    assert high_leverage_flag(6.0, "Financials") is False


def test_icr_warning_flag_low():
    assert icr_warning_flag(1.2) is True
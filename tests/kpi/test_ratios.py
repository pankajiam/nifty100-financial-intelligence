from src.analytics.ratios import (
    net_profit_margin, operating_profit_margin, opm_crosscheck,
    return_on_equity, return_on_capital_employed, return_on_assets
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
from src.analytics.cashflow_kpis import (
    free_cash_flow, cfo_quality_score, capex_intensity,
    fcf_conversion_rate, capital_allocation_pattern
)


def test_free_cash_flow_normal():
    assert free_cash_flow(500, -200) == 300


def test_cfo_quality_score_high():
    score, label = cfo_quality_score([150, 160], [100, 100])
    assert label == "High Quality"


def test_cfo_quality_score_accrual_risk():
    score, label = cfo_quality_score([30, 40], [100, 100])
    assert label == "Accrual Risk"


def test_cfo_quality_score_zero_pat():
    score, label = cfo_quality_score([100], [0])
    assert score is None
    assert label is None


def test_capex_intensity_asset_light():
    intensity, label = capex_intensity(-20, 1000)
    assert label == "Asset Light"


def test_capex_intensity_capital_intensive():
    intensity, label = capex_intensity(-150, 1000)
    assert label == "Capital Intensive"


def test_fcf_conversion_rate_zero_op_profit():
    assert fcf_conversion_rate(100, 0) is None


def test_capital_allocation_reinvestor():
    cfo_s, cfi_s, cff_s, label = capital_allocation_pattern(500, -200, -100, cfo_over_pat=0.8)
    assert label == "Reinvestor"


def test_capital_allocation_shareholder_returns():
    cfo_s, cfi_s, cff_s, label = capital_allocation_pattern(500, -200, -100, cfo_over_pat=1.2)
    assert label == "Shareholder Returns"


def test_capital_allocation_distress_signal():
    cfo_s, cfi_s, cff_s, label = capital_allocation_pattern(-100, 200, 300)
    assert label == "Distress Signal"
from src.analytics.cagr import compute_cagr


def test_cagr_normal():
    cagr, flag = compute_cagr(100, 200, 5)
    assert flag is None
    assert round(cagr, 2) == round(((200/100) ** (1/5) - 1) * 100, 2)


def test_cagr_turnaround():
    cagr, flag = compute_cagr(-50, 100, 3)
    assert cagr is None
    assert flag == "TURNAROUND"


def test_cagr_decline_to_loss():
    cagr, flag = compute_cagr(100, -50, 3)
    assert cagr is None
    assert flag == "DECLINE_TO_LOSS"


def test_cagr_both_negative():
    cagr, flag = compute_cagr(-100, -50, 3)
    assert cagr is None
    assert flag == "BOTH_NEGATIVE"


def test_cagr_zero_base():
    cagr, flag = compute_cagr(0, 100, 3)
    assert cagr is None
    assert flag == "ZERO_BASE"


def test_cagr_insufficient_years():
    cagr, flag = compute_cagr(100, 200, 0)
    assert cagr is None
    assert flag == "INSUFFICIENT"


def test_cagr_insufficient_missing_start():
    cagr, flag = compute_cagr(None, 200, 3)
    assert cagr is None
    assert flag == "INSUFFICIENT"


def test_cagr_insufficient_missing_end():
    cagr, flag = compute_cagr(100, None, 3)
    assert cagr is None
    assert flag == "INSUFFICIENT"


def test_cagr_positive_positive_exact_value():
    cagr, flag = compute_cagr(1000, 1000, 5)
    assert flag is None
    assert round(cagr, 4) == 0.0


def test_cagr_large_growth():
    cagr, flag = compute_cagr(10, 1000, 10)
    assert flag is None
    assert cagr > 0
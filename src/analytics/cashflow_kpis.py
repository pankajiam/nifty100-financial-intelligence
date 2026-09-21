def free_cash_flow(operating_activity, investing_activity):
    op = operating_activity or 0
    inv = investing_activity or 0
    return op + inv


def cfo_quality_score(cfo_values: list, pat_values: list):
    """
    Averages CFO/PAT ratio over up to 5 years.
    cfo_values and pat_values are lists of matching-length numbers.
    Returns (score, label). None, None if PAT sums to 0 or lists empty.
    """
    ratios = []
    for cfo, pat in zip(cfo_values, pat_values):
        if pat is None or pat == 0 or cfo is None:
            continue
        ratios.append(cfo / pat)

    if not ratios:
        return None, None

    avg_ratio = sum(ratios) / len(ratios)

    if avg_ratio > 1.0:
        label = "High Quality"
    elif avg_ratio >= 0.5:
        label = "Moderate"
    else:
        label = "Accrual Risk"

    return avg_ratio, label


def capex_intensity(investing_activity, sales):
    if sales == 0 or sales is None or investing_activity is None:
        return None, None
    intensity = abs(investing_activity) / sales * 100

    if intensity < 3:
        label = "Asset Light"
    elif intensity <= 8:
        label = "Moderate"
    else:
        label = "Capital Intensive"

    return intensity, label


def fcf_conversion_rate(fcf, operating_profit):
    if operating_profit == 0 or operating_profit is None or fcf is None:
        return None
    return fcf / operating_profit * 100


def capital_allocation_pattern(cfo, cfi, cff, cfo_over_pat=None):
    cfo_sign = "+" if cfo >= 0 else "-"
    cfi_sign = "+" if cfi >= 0 else "-"
    cff_sign = "+" if cff >= 0 else "-"

    key = (cfo_sign, cfi_sign, cff_sign)

    if key == ("+", "-", "-"):
        if cfo_over_pat is not None and cfo_over_pat > 1.0:
            label = "Shareholder Returns"
        else:
            label = "Reinvestor"
    elif key == ("+", "+", "-"):
        label = "Liquidating Assets"
    elif key == ("-", "+", "+"):
        label = "Distress Signal"
    elif key == ("-", "-", "+"):
        label = "Growth Funded by Debt"
    elif key == ("+", "+", "+"):
        label = "Cash Accumulator"
    elif key == ("-", "-", "-"):
        label = "Pre-Revenue"
    elif key == ("+", "-", "+"):
        label = "Mixed"
    else:
        label = "Mixed"

    return cfo_sign, cfi_sign, cff_sign, label
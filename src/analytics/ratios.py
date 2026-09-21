def net_profit_margin(net_profit, sales):
    if sales == 0 or sales is None or net_profit is None:
        return None
    return net_profit / sales * 100


def operating_profit_margin(operating_profit, sales):
    if sales == 0 or sales is None or operating_profit is None:
        return None
    return operating_profit / sales * 100


def opm_crosscheck(computed_opm, reported_opm_percentage):
    """Returns True if the difference exceeds 1%, else False. None if inputs missing."""
    if computed_opm is None or reported_opm_percentage is None:
        return None
    return abs(computed_opm - reported_opm_percentage) > 1


def return_on_equity(net_profit, equity_capital, reserves):
    denom = (equity_capital or 0) + (reserves or 0)
    if denom <= 0 or net_profit is None:
        return None
    return net_profit / denom * 100


def return_on_capital_employed(ebit, equity_capital, reserves, borrowings):
    denom = (equity_capital or 0) + (reserves or 0) + (borrowings or 0)
    if denom <= 0 or ebit is None:
        return None
    return ebit / denom * 100


def return_on_assets(net_profit, total_assets):
    if total_assets == 0 or total_assets is None or net_profit is None:
        return None
    return net_profit / total_assets * 100

def debt_to_equity(borrowings, equity_capital, reserves):
    denom = (equity_capital or 0) + (reserves or 0)
    if borrowings == 0 or borrowings is None:
        return 0
    if denom <= 0:
        return None
    return borrowings / denom


def high_leverage_flag(de_ratio, broad_sector):
    if de_ratio is None:
        return False
    if broad_sector == "Financials":
        return False
    return de_ratio > 5


def interest_coverage_ratio(operating_profit, other_income, interest):
    if interest == 0 or interest is None:
        return None
    op = operating_profit or 0
    oi = other_income or 0
    return (op + oi) / interest


def icr_label(icr_value):
    if icr_value is None:
        return "Debt Free"
    return None


def icr_warning_flag(icr_value):
    if icr_value is None:
        return False
    return icr_value < 1.5


def net_debt(borrowings, investments):
    b = borrowings or 0
    i = investments or 0
    return b - i


def asset_turnover(sales, total_assets):
    if total_assets == 0 or total_assets is None or sales is None:
        return None
    return sales / total_assets
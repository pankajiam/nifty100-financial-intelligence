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
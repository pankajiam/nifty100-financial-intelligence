def compute_cagr(start_value, end_value, n_years):
    """
    Returns (cagr_value, flag). cagr_value is None unless both
    start and end are positive. flag is None on success.
    """
    if n_years is None or n_years <= 0:
        return None, "INSUFFICIENT"

    if start_value is None or end_value is None:
        return None, "INSUFFICIENT"

    if start_value == 0:
        return None, "ZERO_BASE"

    if start_value > 0 and end_value > 0:
        cagr = ((end_value / start_value) ** (1 / n_years) - 1) * 100
        return cagr, None

    if start_value > 0 and end_value < 0:
        return None, "DECLINE_TO_LOSS"

    if start_value < 0 and end_value > 0:
        return None, "TURNAROUND"

    if start_value < 0 and end_value < 0:
        return None, "BOTH_NEGATIVE"

    return None, "ZERO_BASE"


def cagr_from_series(values_by_year: dict, n_years: int):
    """
    values_by_year: {year_str: value}. Picks the earliest and latest
    year that are exactly n_years apart if possible, else uses
    earliest/latest available with INSUFFICIENT flag if too few years.
    """
    years = sorted(values_by_year.keys())
    if len(years) < 2:
        return None, "INSUFFICIENT"

    span = years[-1]
    start_year_index = len(years) - 1 - n_years
    if start_year_index < 0:
        return None, "INSUFFICIENT"

    start_year = years[start_year_index]
    end_year = years[-1]

    return compute_cagr(values_by_year[start_year], values_by_year[end_year], n_years)
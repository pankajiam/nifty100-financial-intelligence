import yaml
import pandas as pd


def load_config(config_path="config/screener_config.yaml"):
    with open(config_path) as f:
        return yaml.safe_load(f)


def apply_filter(df, column, direction, threshold, sector_col=None, skip_financials=False):
    result = df.copy()

    if skip_financials and sector_col in result.columns:
        financials_mask = result[sector_col] == "Financials"
    else:
        financials_mask = pd.Series(False, index=result.index)

    if column == "interest_coverage":
        icr_infinite_mask = result[column].isna() & (result.get("icr_label") == "Debt Free")
    else:
        icr_infinite_mask = pd.Series(False, index=result.index)

    if direction == "min":
        passes = result[column] >= threshold
    else:
        passes = result[column] <= threshold

    passes = passes | financials_mask | icr_infinite_mask
    return result[passes]


def run_filters(df, filters: dict, config: dict, sector_col="broad_sector"):
    """
    filters: {"roe_min": 15, "de_max": 1.0, ...} -- keys matching config.
    """
    result = df.copy()
    for filter_key, threshold in filters.items():
        if filter_key not in config["filters"]:
            continue
        rule = config["filters"][filter_key]
        column = rule["column"]
        direction = rule["direction"]

        skip_financials = (column == "debt_to_equity" and direction == "max")

        result = apply_filter(
            result, column, direction, threshold,
            sector_col=sector_col, skip_financials=skip_financials
        )

    return result.sort_values("composite_quality_score", ascending=False)
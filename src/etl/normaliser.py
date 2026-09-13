import pandas as pd

import re


def normalize_ticker(ticker: str) -> str:
    """Normalize a company ticker."""
    return ticker.strip().upper()


def normalize_year(year: str) -> str:
    """Normalize a financial year label."""
    value = year.strip()

    if re.fullmatch(r"\d{4}-\d{2}", value):
        return value

    if re.fullmatch(r"\d{4}", value):
        return f"{value}-03"

    if re.fullmatch(r"FY\d{2}", value, re.IGNORECASE):
        return f"20{value[-2:]}-03"

    match = re.fullmatch(r"([A-Za-z]+)[ -](\d{2,4})", value)

    if match:
        month = match.group(1)
        year_part = match.group(2)

        months = {
            "jan": "01",
            "feb": "02",
            "mar": "03",
            "apr": "04",
            "may": "05",
            "jun": "06",
            "jul": "07",
            "aug": "08",
            "sep": "09",
            "oct": "10",
            "nov": "11",
            "dec": "12",
        }

        month_number = months.get(month.lower()[:3])

        if month_number is None:
            return "PARSE_ERROR"

        if len(year_part) == 2:
            year_part = f"20{year_part}"

        return f"{year_part}-{month_number}"

    return "PARSE_ERROR"

def normalize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize ticker and year columns when they are present."""
    if "company_id" in df.columns:
        df["company_id"] = df["company_id"].map(normalize_ticker)

    if "year" in df.columns:
        df["year"] = df["year"].map(normalize_year)

    return df

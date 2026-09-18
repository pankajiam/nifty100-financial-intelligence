import pandas as pd
from src.etl.normaliser import normalize_ticker, normalize_year, normalize_dataframe


def test_normalize_ticker_uppercase():
    assert normalize_ticker("tcs") == "TCS"


def test_normalize_ticker_removes_spaces():
    assert normalize_ticker("  tcs  ") == "TCS"


def test_normalize_year_already_normalized():
    assert normalize_year("2023-03") == "2023-03"


def test_normalize_year_plain_year():
    assert normalize_year("2023") == "2023-03"


def test_normalize_year_month_year():
    assert normalize_year("Mar-23") == "2023-03"

def test_normalize_year_full_month():
    assert normalize_year("March-2023") == "2023-03"


def test_normalize_year_december():
    assert normalize_year("Dec-22") == "2022-12"


def test_normalize_year_june():
    assert normalize_year("Jun-23") == "2023-06"


def test_normalize_year_fy_format():
    assert normalize_year("FY23") == "2023-03"


def test_normalize_year_lowercase_fy():
    assert normalize_year("fy23") == "2023-03"

def test_normalize_ticker_mixed_case():
    assert normalize_ticker("TcS") == "TCS"


def test_normalize_ticker_multiple_spaces():
    assert normalize_ticker("   HDFC   ") == "HDFC"


def test_normalize_year_march_with_space():
    assert normalize_year("Mar 23") == "2023-03"


def test_normalize_year_december_with_space():
    assert normalize_year("Dec 2023") == "2023-12"


def test_normalize_year_september():
    assert normalize_year("Sep 2024") == "2024-09"

def test_normalize_year_invalid_value():
    assert normalize_year("garbage") == "PARSE_ERROR"


def test_normalize_year_invalid_month():
    assert normalize_year("XYZ-23") == "PARSE_ERROR"


def test_normalize_year_ttm():
    assert normalize_year("TTM") == "PARSE_ERROR"


def test_normalize_year_nine_month_format():
    assert normalize_year("Mar 2016 9m") == "PARSE_ERROR"


def test_normalize_year_fifteen_month_format():
    assert normalize_year("Mar 2023 15") == "PARSE_ERROR"

def test_normalize_dataframe_normalizes_company_id():
    df = pd.DataFrame({"company_id": ["  tcs  ", "infy"], "year": ["2023", "2024"]})
    result = normalize_dataframe(df)
    assert result["company_id"].tolist() == ["TCS", "INFY"]


def test_normalize_dataframe_normalizes_year():
    df = pd.DataFrame({"company_id": ["TCS"], "year": ["Mar-23"]})
    result = normalize_dataframe(df)
    assert result["year"].tolist() == ["2023-03"]


def test_normalize_dataframe_missing_company_id_column():
    df = pd.DataFrame({"year": ["2023"]})
    result = normalize_dataframe(df)
    assert result["year"].tolist() == ["2023-03"]


def test_normalize_dataframe_missing_year_column():
    df = pd.DataFrame({"company_id": [" tcs "]})
    result = normalize_dataframe(df)
    assert result["company_id"].tolist() == ["TCS"]


def test_normalize_dataframe_no_relevant_columns():
    df = pd.DataFrame({"sales": [100, 200]})
    result = normalize_dataframe(df)
    assert result["sales"].tolist() == [100, 200]


def test_normalize_ticker_with_numbers():
    assert normalize_ticker("m&m") == "M&M"


def test_normalize_year_two_digit_fy_leading_zero():
    assert normalize_year("FY05") == "2005-03"


def test_normalize_year_dec_full_year_with_space():
    assert normalize_year("December 2022") == "2022-12"


def test_normalize_year_empty_string():
    assert normalize_year("") == "PARSE_ERROR"


def test_normalize_ticker_already_clean():
    assert normalize_ticker("RELIANCE") == "RELIANCE"

def test_normalize_year_no_space_month_year():
    assert normalize_year("Mar2021") == "2021-03"
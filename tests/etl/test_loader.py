from src.etl.loader import load_excel


def test_load_profitandloss():
    df = load_excel("data/raw/profitandloss.xlsx")

    assert not df.empty
    assert "company_id" in df.columns
    assert "year" in df.columns
    assert "sales" in df.columns

def test_load_excel_missing_file():
    try:
        load_excel("data/raw/does_not_exist.xlsx")
        assert False
    except FileNotFoundError:
        assert True


def test_load_excel_empty_path():
    try:
        load_excel("")
        assert False
    except FileNotFoundError:
        assert True

def test_load_balancesheet():
    df = load_excel("data/raw/balancesheet.xlsx")
    assert not df.empty
    assert "company_id" in df.columns
    assert "year" in df.columns
    assert "total_assets" in df.columns


def test_load_companies():
    df = load_excel("data/raw/companies.xlsx")
    assert not df.empty
    assert "company_name" in df.columns
    assert "roce_percentage" in df.columns


def test_load_balancesheet_returns_dataframe_type():
    import pandas as pd
    df = load_excel("data/raw/balancesheet.xlsx")
    assert isinstance(df, pd.DataFrame)
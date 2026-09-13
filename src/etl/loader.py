from pathlib import Path

import pandas as pd

def load_excel(file_path: str) -> pd.DataFrame:
    """Load an Excel file into a DataFrame."""
    path = Path(file_path)

    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"Excel file not found: {file_path}")

    df = pd.read_excel(path, header=1)

    if df.empty or len(df.columns) == 0:
        raise ValueError(f"Excel file contains no usable data: {file_path}")

    return df
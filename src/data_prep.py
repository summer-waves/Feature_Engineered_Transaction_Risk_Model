from pathlib import Path
import pandas as pd

def load_transactions(path: Path, n_rows: int | None = None, sample_frac: float | None = None) -> pd.DataFrame:
    df = pd.read_csv(path)

    if n_rows is not None:
        df = df.head(n_rows)
    elif sample_frac is not None:
        df = df.sample(frac=sample_frac, random_state=42)

    return df
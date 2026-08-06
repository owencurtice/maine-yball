import pandas as pd

DIGEST_COLUMNS = ["Week", "Title", "Text"]

def load_digest(path="data/digest.csv"):
    try:
        df = pd.read_csv(path)
        return df.sort_values("Week")
    except (pd.errors.EmptyDataError, FileNotFoundError):
        return pd.DataFrame(columns=DIGEST_COLUMNS)

def latest_entry(df):
    if df.empty:
        return None
    return df.iloc[-1]
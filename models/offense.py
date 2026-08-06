import numpy as np

def offensive_rating(df):
    games = df["Wins"] + df["Losses"]
    raw = np.where(games > 0, df["Points_For"] / games, 0.0)

    spread = raw.max() - raw.min()
    df["Offensive_Rating"] = (raw - raw.min()) / spread if spread != 0 else 0.5

    return df
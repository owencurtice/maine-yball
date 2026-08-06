import numpy as np

def defensive_rating(df):
    games = df["Wins"] + df["Losses"]
    raw = np.where(games > 0, df["Points_Against"] / games, 0.0)

    spread = raw.max() - raw.min()
    df["Defensive_Rating"] = (raw.max() - raw) / spread if spread != 0 else 0.5

    return df
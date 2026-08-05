def defensive_rating(df):
    games = df["Wins"] + df["Losses"]
    raw = df["Points_Against"] / games

    spread = raw.max() - raw.min()
    df["Defensive_Rating"] = (raw.max() - raw) / spread if spread != 0 else 0.5

    return df
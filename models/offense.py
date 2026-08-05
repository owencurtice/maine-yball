def offensive_rating(df):
    games = df["Wins"] + df["Losses"]
    raw = df["Points_For"] / games

    spread = raw.max() - raw.min()
    df["Offensive_Rating"] = (raw - raw.min()) / spread if spread != 0 else 0.5

    return df
import numpy as np

def winning_percentage(df):
    games = df["Wins"] + df["Losses"]
    df["Winning_Percentage"] = np.where(games > 0, df["Wins"] / games, 0.0)
    return df
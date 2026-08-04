def strength_of_schedule(df):

    df["SOS"] = df["Opponent_Win_Percentage"]

    return df
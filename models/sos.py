def strength_of_schedule(df):
    win_pct = dict(zip(df["TeamID"], df["Winning_Percentage"]))

    df["SOS"] = df["Opponents"].apply(
        lambda opps: sum(win_pct.get(o, 0.5) for o in opps) / len(opps) if opps else 0.5
    )
    return df

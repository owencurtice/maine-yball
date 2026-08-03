def calculate_mpi(df):

    df["Win_Percentage"] = (
        df["Wins"] /
        (df["Wins"] + df["Losses"])
    )

    df["MPI"] = (
        (df["Win_Percentage"] * 50)
        +
        (df["Opponent_Win_Percentage"] * 30)
    )

    return df

def offensive_rating(df):

    df["Offensive_Rating"] = (

        df["Points_For"]

        /

        (df["Wins"] + df["Losses"])

    )

    return df
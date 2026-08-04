def winning_percentage(df):

    df["Winning_Percentage"] = (

        df["Wins"]

        /

        (

            df["Wins"]

            +

            df["Losses"]

        )

    )

    return df
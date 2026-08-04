def defensive_rating(df):

    games = df["Wins"] + df["Losses"]

    df["Defensive_Rating"] = (

        50

        -

        (

            df["Points_Against"]

            /

            games

        )

    )

    return df
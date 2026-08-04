def efficiency(df):

    df["Efficiency"] = (

        df["Points_For"]

        /

        df["Points_Against"]

    )

    return df
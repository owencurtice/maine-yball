def point_differential(df):

    df["Point_Differential"] = (

        df["Points_For"]

        -

        df["Points_Against"]

    )

    return df
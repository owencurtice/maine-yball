from models.winning import winning_percentage

from models.sos import strength_of_schedule

from models.point_diff import point_differential

from models.efficiency import efficiency

from models.offense import offensive_rating
from models.defense import defensive_rating

def calculate_mpi(df):

    df = winning_percentage(df)

    df = strength_of_schedule(df)

    df = point_differential(df)

    df = efficiency(df)

    df = offensive_rating(df)

    df = defensive_rating(df)

    df["MPI"] = (

        df["Winning_Percentage"] * 0.40

    +

        df["SOS"] * 0.30

    +

        df["Offensive_Rating"] * 0.15

    +

        df["Defensive_Rating"] * 0.15

)

    return df
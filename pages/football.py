import streamlit as st
import pandas as pd

from models.mpi import calculate_mpi


st.title("🏈 Football Intelligence Center")

st.write(
"""
Analyzing Maine football through data,
competition strength, and predictive analytics.
"""
)


df = pd.read_csv(
    "data/football_stats.csv"
)


df = calculate_mpi(df)


rankings = df.sort_values(
    "MPI",
    ascending=False
)


st.header("🏆 Maine-yball Power Index")


st.dataframe(
    rankings[
        [
            "Team",
            "Wins",
            "Losses",
            "MPI"
        ]
    ]
)
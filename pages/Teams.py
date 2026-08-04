import streamlit as st
import pandas as pd

st.title("Teams")

teams = pd.read_csv("data/teams.csv")

division = st.selectbox(
    "Division",
    [
        "All",
        "A North",
        "A South",
        "B North",
        "B South"
    ]
)

if division != "All":
    teams = teams[teams["Division"] == division]

st.dataframe(teams)
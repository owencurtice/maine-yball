import streamlit as st
import pandas as pd

df = pd.read_csv("data/football_stats.csv")

st.title("League Statistics")

st.dataframe(df)

st.bar_chart(
    df,
    x="Team",
    y="Points_For"
)

st.bar_chart(
    df,
    x="Team",
    y="Points_Against"
)
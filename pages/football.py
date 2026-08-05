import streamlit as st
import pandas as pd

from models.mpi import calculate_mpi

from utils.components import ranking_card
from utils.charts import mpi_chart
import altair as alt
# ------------------------
# Page Header
# ------------------------

st.title("🏈 Football")

st.caption(
    "Weekly rankings, advanced metrics, and evidence-based analysis of Maine high school football."
)

st.divider()

# ------------------------
# Load Data
# ------------------------

df = pd.read_csv("data/football_stats.csv")

df = calculate_mpi(df)

rankings = df.sort_values(
    "MPI",
    ascending=False
)

# ------------------------
# Top Team
# ------------------------

top_team = rankings.iloc[0]

col1, col2, col3 = st.columns(3)

def mpi_chart(df):
    chart = (
        alt.Chart(df)
        .mark_bar(color="#C9A227")
        .encode(
            x=alt.X("MPI:Q", title="MPI"),
            y=alt.Y("Team:N", sort="-x", title=None),
            tooltip=["Team", "MPI"]
        )
        .properties(height=alt.Step(35))
    )
    st.altair_chart(chart, use_container_width=True)
    
with col1:
    st.metric(
        "Current #1",
        top_team["Team"]
    )

with col2:
    st.metric(
        "MPI",
        round(top_team["MPI"], 1)
    )

with col3:
    st.metric(
        "Record",
        f"{top_team['Wins']}-{top_team['Losses']}"
    )

st.divider()

# ------------------------
# Rankings Table
# ------------------------

st.header("Current Rankings")

rankings = rankings.reset_index(drop=True)

rankings["Rank"] = rankings.index + 1

for _, team in rankings.iterrows():

    ranking_card(team)

st.divider()

st.header("MPI Rankings")

mpi_chart(rankings)
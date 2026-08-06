import streamlit as st
import pandas as pd

from models.mpi import calculate_mpi
from utils.stats import build_team_stats
from utils.components import ranking_card
from utils.charts import mpi_chart

# ------------------------
# Page Header
# ------------------------

st.title("🏈 Football")

st.caption(
    "Weekly rankings, advanced metrics, and evidence-based analysis of Maine high school football."
)

st.divider()

# ------------------------
# Build Rankings from games.csv
# ------------------------

from utils.data import load_games, load_teams

teams = load_teams()
games = load_games()

stats = build_team_stats(games, teams)
stats = calculate_mpi(stats)

rankings = stats.merge(teams[["TeamID", "School"]], on="TeamID")
rankings = rankings.rename(columns={"School": "Team"})
rankings = rankings.sort_values("MPI", ascending=False).reset_index(drop=True)
rankings["Rank"] = rankings.index + 1

# ------------------------
# Top Team
# ------------------------

top_team = rankings.iloc[0]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Current #1", top_team["Team"])

with col2:
    st.metric("MPI", round(top_team["MPI"], 1))

with col3:
    st.metric("Record", f"{int(top_team['Wins'])}-{int(top_team['Losses'])}")

st.divider()

# ------------------------
# Rankings Table
# ------------------------

st.header("Current Rankings")

for _, team in rankings.iterrows():
    ranking_card(team)

st.divider()

st.header("MPI Rankings")

mpi_chart(rankings)
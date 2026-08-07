import streamlit as st

from utils.theme import inject_theme
from utils.data import load_games, load_teams
from utils.rankings import get_rankings
from utils.components import ranking_card
from utils.charts import mpi_chart
from utils.history import get_movers

inject_theme()

st.title("🏈 Football")
st.caption("Weekly rankings, advanced metrics, and evidence-based analysis of Maine high school football.")
st.divider()

teams = load_teams()
games = load_games()

rankings, season_started = get_rankings(games, teams)

if not season_started:
    st.info("Preseason Power Rankings — based on 2025 playoff performance. Live MPI begins once Week 1 results are in.")

top_team = rankings.iloc[0]

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Current #1", top_team["Team"])
with col2:
    st.metric("MPI", round(top_team["MPI"], 1))
with col3:
    st.metric("Record", f"{int(top_team['Wins'])}-{int(top_team['Losses'])}")

st.divider()
st.header("Current Rankings")

for _, team in rankings.iterrows():
    ranking_card(team)

st.divider()

movers = get_movers(games, teams)
if movers:
    st.divider()
    st.header("Biggest Movers")
    st.caption(f"Change since {movers['baseline_label']}")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Risers")
        for _, row in movers["risers"].iterrows():
            mover_card(row["Team"], row["Delta"], row["MPI"])
    with col2:
        st.subheader("Fallers")
        for _, row in movers["fallers"].iterrows():
            mover_card(row["Team"], row["Delta"], row["MPI"])

st.header("MPI Rankings")
mpi_chart(rankings)

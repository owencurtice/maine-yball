import streamlit as st
import pandas as pd

from utils.stats import build_team_stats

from utils.data import load_games, load_teams

teams = load_teams()
games = load_games()

stats = build_team_stats(games, teams)
stats = stats.merge(teams[["TeamID", "School"]], on="TeamID")
stats = stats.rename(columns={"School": "Team"})

st.title("League Statistics")

display_cols = ["Team", "Wins", "Losses", "Points_For", "Points_Against"]
st.dataframe(stats[display_cols])

st.bar_chart(
    stats,
    x="Team",
    y="Points_For"
)

st.bar_chart(
    stats,
    x="Team",
    y="Points_Against"
)
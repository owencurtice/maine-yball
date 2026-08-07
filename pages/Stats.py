import streamlit as st

from utils.theme import inject_theme
from utils.data import load_games, load_teams
from utils.rankings import get_rankings
from utils.charts import offense_defense_quadrant

inject_theme()

st.title("League Statistics")

teams = load_teams()
games = load_games()

rankings, season_started = get_rankings(games, teams)

display_cols = ["Team", "Wins", "Losses", "Points_For", "Points_Against"]
st.dataframe(rankings[display_cols], hide_index=True)

st.bar_chart(rankings, x="Team", y="Points_For")
st.bar_chart(rankings, x="Team", y="Points_Against")

st.divider()
st.subheader("Offense vs. Defense")

if season_started:
    st.caption("Each dot is a team. Top-right = elite on both sides of the ball. Bottom-left = struggling on both.")
    offense_defense_quadrant(rankings)
else:
    st.info("This chart becomes available once live MPI data begins after Week 1.")
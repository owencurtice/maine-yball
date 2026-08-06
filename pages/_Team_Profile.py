import streamlit as st
import pandas as pd

from utils.theme import inject_theme
from utils.data import load_games, load_teams
from models.mpi import calculate_mpi
from utils.stats import build_team_stats

inject_theme()

teams = load_teams()
games = load_games()

team_id = st.session_state.get("selected_team")

if team_id is None:
    st.warning("No team selected. Go back to the Teams page and pick one.")
    st.stop()

team = teams[teams["TeamID"] == team_id].iloc[0]

st.image(f"assets/logos/{team['Logo']}", width=150)
st.title(team["School"])
st.caption(f"{team['Mascot']} — {team['Class']} {team['Region']} ({team['Division']})")

st.divider()

stats = build_team_stats(games, teams)
stats = calculate_mpi(stats)
row = stats[stats["TeamID"] == team_id].iloc[0]

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Record", f"{int(row['Wins'])}-{int(row['Losses'])}")
with col2:
    st.metric("MPI", round(row["MPI"], 1))
with col3:
    st.metric("Games Played", int(row["Wins"] + row["Losses"]))

st.divider()
st.subheader("Schedule")

id_to_school = dict(zip(teams["TeamID"], teams["School"]))
team_games = games[
    (games["HomeID"] == team_id) | (games["AwayID"] == team_id)
].sort_values("Week")

for _, g in team_games.iterrows():
    is_home = g["HomeID"] == team_id
    opp_id = g["AwayID"] if is_home else g["HomeID"]
    opp_name = g["OpponentName"] if opp_id == "OOC" else id_to_school.get(opp_id, opp_id)
    site = "vs" if is_home else "@"

    if g["Status"] == "Final":
        team_score = g["HomeScore"] if is_home else g["AwayScore"]
        opp_score = g["AwayScore"] if is_home else g["HomeScore"]
        result = "W" if team_score > opp_score else "L"
        st.write(f"Week {g['Week']}: {site} {opp_name} — {result} {int(team_score)}-{int(opp_score)}")
    else:
        date_display = g["Date"] if g["Date"] else "TBD"
        st.write(f"Week {g['Week']}: {site} {opp_name} — {date_display}")
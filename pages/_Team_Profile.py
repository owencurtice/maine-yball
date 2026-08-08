import streamlit as st

from utils.theme import inject_theme
from utils.data import load_games, load_teams
from utils.rankings import get_rankings
from utils.components import mpi_scorecard
from utils.elo import compute_elo_timeline

inject_theme()

teams = load_teams()
id_to_school = dict(zip(teams["TeamID"], teams["School"]))

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

rankings, season_started = get_rankings(games, teams)
row = rankings[rankings["TeamID"] == team_id].iloc[0]

elo_entering_week, current_elo, predictions = compute_elo_timeline(games, teams)
team_elo = round(current_elo.get(team_id, 1500))

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Record", f"{int(row['Wins'])}-{int(row['Losses'])}")
with col2:
    st.metric("MPI", round(row["MPI"], 1))
with col3:
    st.metric("Elo", team_elo)
with col4:
    st.metric("Rank", f"#{int(row['Rank'])}")
st.divider()

if season_started:
    st.subheader("MPI Scorecard")
    st.caption("Full transparency on how this team's ranking is calculated.")
    mpi_scorecard(row)
else:
    st.info("The full MPI breakdown becomes available once Week 1 results are in. Right now this team's score reflects last year's playoff finish.")

st.divider()
st.subheader("Next Game Prediction")

upcoming = predictions[
    ((predictions["HomeID"] == team_id) | (predictions["AwayID"] == team_id)) &
    (predictions["Status"] != "Final")
].sort_values("Week")

if upcoming.empty:
    st.caption("No upcoming games on the schedule.")
else:
    g = upcoming.iloc[0]
    is_home = g["HomeID"] == team_id
    opp_id = g["AwayID"] if is_home else g["HomeID"]
    opp_name = id_to_school.get(opp_id, opp_id) if opp_id != "OOC" else "Non-Conference Opponent"

    team_prob = g["HomeWinProb"] if is_home else g["AwayWinProb"]
    pct = round(team_prob * 100)

    st.markdown(f"**Week {int(g['Week'])}** vs **{opp_name}**")
    st.progress(pct / 100)
    st.caption(f"{team['School']} win probability: {pct}%")
st.divider()
st.subheader("Schedule")

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

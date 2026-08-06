import streamlit as st
import pandas as pd
from datetime import date
from io import BytesIO

from utils.theme import inject_theme
from utils.auth import require_admin_password
from utils.data import load_games, load_teams
from models.mpi import calculate_mpi
from utils.stats import build_team_stats
from utils.graphics import generate_ranking_graphic

inject_theme()

st.title("Admin")

require_admin_password()

teams = load_teams()
games = load_games()
games_path = "data/games.csv"

team_options = dict(zip(teams["School"], teams["TeamID"]))

tab1, tab2, tab3 = st.tabs(["Add Games", "Enter Scores", "Graphics"])

# ------------------------
# TAB 1: Add Games
# ------------------------
with tab1:
    st.subheader("Add a Game to the Schedule")

    week = st.number_input("Week", min_value=1, max_value=15, step=1)
    game_date = st.date_input("Date", value=date.today())
    home_school = st.selectbox("Home Team", team_options.keys(), key="home_add")
    away_school = st.selectbox("Away Team", team_options.keys(), key="away_add")

    home_id = team_options[home_school]
    away_id = team_options[away_school]
    division = teams.loc[teams["TeamID"] == home_id, "Division"].values[0]

    if st.button("Add Game"):
        if home_id == away_id:
            st.error("Home and away team can't be the same.")
        else:
            week_games = games[games["Week"] == week]
            game_num = len(week_games) + 1
            game_id = f"2026-W{int(week):02d}-{game_num:03d}"

            new_row = pd.DataFrame([{
                "GameID": game_id, "Week": week, "Date": game_date,
                "HomeID": home_id, "AwayID": away_id, "OpponentName": "",
                "Division": division, "Status": "Scheduled",
                "HomeScore": "", "AwayScore": "", "IsConference": True
            }])

            games = pd.concat([games, new_row], ignore_index=True)
            games.to_csv(games_path, index=False)
            st.success(f"Added {home_school} vs {away_school} — {game_id}")

# ------------------------
# TAB 2: Enter Scores
# ------------------------
with tab2:
    st.subheader("Enter Friday Night Scores")

    if games.empty:
        st.info("No games scheduled yet. Add some in the first tab.")
    else:
        pending = games[games["Status"] != "Final"]

        if pending.empty:
            st.info("All games have final scores entered.")
        else:
            week_filter = st.selectbox("Week", sorted(pending["Week"].unique()))
            week_games = pending[pending["Week"] == week_filter]

            id_to_school = dict(zip(teams["TeamID"], teams["School"]))
            id_to_school["OOC"] = "Non-Conference"

            labels = {}
            for _, row in week_games.iterrows():
                home_name = row["OpponentName"] if row["HomeID"] == "OOC" else id_to_school[row["HomeID"]]
                away_name = row["OpponentName"] if row["AwayID"] == "OOC" else id_to_school[row["AwayID"]]
                labels[row["GameID"]] = f"{home_name} vs {away_name}"

            selected_id = st.selectbox(
                "Game", options=labels.keys(), format_func=lambda gid: labels[gid]
            )

            home_score = st.number_input("Home Score", min_value=0, step=1)
            away_score = st.number_input("Away Score", min_value=0, step=1)

            if st.button("Save Score"):
                idx = games[games["GameID"] == selected_id].index[0]
                games.at[idx, "HomeScore"] = home_score
                games.at[idx, "AwayScore"] = away_score
                games.at[idx, "Status"] = "Final"
                games.to_csv(games_path, index=False)
                st.success(f"Saved: {labels[selected_id]} — {home_score}-{away_score}")

# ------------------------
# TAB 3: Graphics
# ------------------------
with tab3:
    st.subheader("Generate Weekly Graphic")

    stats = build_team_stats(games, teams)
    stats = calculate_mpi(stats)
    rankings = stats.merge(teams[["TeamID", "School", "Class"]], on="TeamID")
    rankings = rankings.rename(columns={"School": "Team"})

    class_filter = st.selectbox("Class", ["All", "A", "B"])

    if class_filter != "All":
        rankings = rankings[rankings["Class"] == class_filter]

    rankings = rankings.sort_values("MPI", ascending=False).reset_index(drop=True)
    rankings["Rank"] = rankings.index + 1

    subtitle = f"Class {class_filter}" if class_filter != "All" else ""

    if st.button("Generate Graphic"):
        img = generate_ranking_graphic(rankings, title="Weekly Rankings", subtitle=subtitle)

        buf = BytesIO()
        img.save(buf, format="PNG")

        st.image(img)
        st.download_button(
            "Download for Instagram", data=buf.getvalue(),
            file_name="maineyball_rankings.png", mime="image/png"
        )
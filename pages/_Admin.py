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
from utils.rankings import get_rankings
from utils.history import save_snapshot
from utils.history import get_movers
from utils.graphics import generate_movers_graphic
from utils.graphics import generate_quote_graphic
from utils.schedule_strength import compute_schedule_strength
from utils.graphics import generate_schedule_strength_graphic
from utils.elo import get_elo_rankings
from utils.db import get_supabase

inject_theme()

st.title("Admin")

require_admin_password()

teams = load_teams()
games = load_games()

team_options = dict(zip(teams["School"], teams["TeamID"]))

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(
    [
        "Add Games",
        "Enter Scores",
        "Edit Schedule",
        "Graphics",
        "Movers Graphic",
        "Custom Post",
        "Schedule Strength",
        "Elo Rankings"
    ]
)
)

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

            supabase = get_supabase()
            supabase.table("games").insert({
                "GameID": game_id,
                "Week": int(week),
                "Date": game_date.isoformat(),
                "HomeID": home_id,
                "AwayID": away_id,
                "OpponentName": "",
                "Division": division,
                "Status": "Scheduled",
                "HomeScore": None,
                "AwayScore": None,
                "IsConference": True
            }).execute()
            st.success(f"Added {home_school} vs {away_school} — {game_id}")
            st.rerun()

# ------------------------
# TAB 2: Enter / Edit Scores
# ------------------------
with tab2:
    st.subheader("Enter Friday Night Scores")

    if games.empty:
        st.info("No games scheduled yet. Add some in the first tab.")
    else:

        # ========================
        # ENTER NEW SCORE
        # ========================
        st.markdown("### Enter Score")

        pending = games[games["Status"] != "Final"]

        if pending.empty:
            st.info("All scheduled games have final scores entered.")
        else:
            week_filter = st.selectbox(
                "Week",
                sorted(pending["Week"].unique()),
                key="score_week"
            )

            week_games = pending[pending["Week"] == week_filter]

            id_to_school = dict(zip(teams["TeamID"], teams["School"]))
            id_to_school["OOC"] = "Non-Conference"

            labels = {}

            for _, row in week_games.iterrows():
                home_name = (
                    row["OpponentName"]
                    if row["HomeID"] == "OOC"
                    else id_to_school[row["HomeID"]]
                )

                away_name = (
                    row["OpponentName"]
                    if row["AwayID"] == "OOC"
                    else id_to_school[row["AwayID"]]
                )

                labels[row["GameID"]] = f"{home_name} vs {away_name}"

            selected_id = st.selectbox(
                "Game",
                options=labels.keys(),
                format_func=lambda gid: labels[gid],
                key="new_score_game"
            )

            home_score = st.number_input(
                "Home Score",
                min_value=0,
                step=1,
                key="new_home_score"
            )

            away_score = st.number_input(
                "Away Score",
                min_value=0,
                step=1,
                key="new_away_score"
            )

            if st.button("Save Score", key="save_new_score"):

                supabase = get_supabase()
                supabase.table("games").update({
                    "HomeScore": int(home_score),
                    "AwayScore": int(away_score),
                    "Status": "Final"
                }).eq("GameID", selected_id).execute()

                idx = games[games["GameID"] == selected_id].index[0]
                week_saved = int(games.at[idx, "Week"])

                updated_rankings, _ = get_rankings(games, teams)
                save_snapshot(week_saved, updated_rankings)

                st.success(
                    f"Saved: {labels[selected_id]} — "
                    f"{home_score}-{away_score}"
                )

                st.rerun()


        # ========================
        # EDIT EXISTING SCORE
        # ========================
        st.divider()
        st.markdown("### Edit Existing Score")

        completed = games[games["Status"] == "Final"].copy()

        if completed.empty:
            st.info("No final scores have been entered yet.")
        else:

            id_to_school = dict(zip(teams["TeamID"], teams["School"]))
            id_to_school["OOC"] = "Non-Conference"

            completed_labels = {}

            for _, row in completed.iterrows():

                home_name = (
                    row["OpponentName"]
                    if row["HomeID"] == "OOC"
                    else id_to_school[row["HomeID"]]
                )

                away_name = (
                    row["OpponentName"]
                    if row["AwayID"] == "OOC"
                    else id_to_school[row["AwayID"]]
                )

                completed_labels[row["GameID"]] = (
                    f"Week {int(row['Week'])}: "
                    f"{home_name} {int(row['HomeScore'])}-"
                    f"{int(row['AwayScore'])} {away_name}"
                )

            edit_game_id = st.selectbox(
                "Select game to edit",
                options=completed_labels.keys(),
                format_func=lambda gid: completed_labels[gid],
                key="edit_game"
            )

            edit_idx = games[games["GameID"] == edit_game_id].index[0]
            edit_game = games.loc[edit_idx]

            current_home = int(edit_game["HomeScore"])
            current_away = int(edit_game["AwayScore"])

            col1, col2 = st.columns(2)

            with col1:
                new_home_score = st.number_input(
                    "Home Score",
                    min_value=0,
                    value=current_home,
                    step=1,
                    key="edit_home_score"
                )

            with col2:
                new_away_score = st.number_input(
                    "Away Score",
                    min_value=0,
                    value=current_away,
                    step=1,
                    key="edit_away_score"
                )

            if st.button("Update Score", key="update_score"):

                supabase = get_supabase()
                supabase.table("games").update({
                    "HomeScore": int(new_home_score),
                    "AwayScore": int(new_away_score),
                    "Status": "Final"
                }).eq("GameID", edit_game_id).execute()

                week_saved = int(games.at[edit_idx, "Week"])

                updated_rankings, _ = get_rankings(games, teams)
                save_snapshot(week_saved, updated_rankings)

                st.success(
                    f"Updated score to "
                    f"{new_home_score}-{new_away_score}"
                )

                st.rerun()

# ------------------------
# TAB 3: Edit Schedule
# ------------------------
with tab3:
    st.subheader("Edit Schedule")

    if games.empty:
        st.info("No games scheduled.")
    else:
        id_to_school = dict(zip(teams["TeamID"], teams["School"]))
        id_to_school["OOC"] = "Non-Conference"

        schedule_labels = {}

        for _, row in games.iterrows():
            home_name = (
                row["OpponentName"]
                if row["HomeID"] == "OOC"
                else id_to_school.get(row["HomeID"], row["HomeID"])
            )

            away_name = (
                row["OpponentName"]
                if row["AwayID"] == "OOC"
                else id_to_school.get(row["AwayID"], row["AwayID"])
            )

            schedule_labels[row["GameID"]] = (
                f"Week {int(row['Week'])}: "
                f"{home_name} vs {away_name} "
                f"({row['Date']})"
            )

        selected_game_id = st.selectbox(
            "Select game",
            options=schedule_labels.keys(),
            format_func=lambda gid: schedule_labels[gid],
            key="schedule_edit_game"
        )

        selected_idx = games[games["GameID"] == selected_game_id].index[0]
        selected_game = games.loc[selected_idx]

        st.divider()

        st.markdown("### Change Game")

        home_options = list(team_options.keys())
        away_options = list(team_options.keys())

        current_home_school = id_to_school.get(
            selected_game["HomeID"],
            selected_game["HomeID"]
        )

        current_away_school = id_to_school.get(
            selected_game["AwayID"],
            selected_game["AwayID"]
        )

        new_home_school = st.selectbox(
            "Home Team",
            home_options,
            index=(
                home_options.index(current_home_school)
                if current_home_school in home_options
                else 0
            ),
            key="schedule_new_home"
        )

        new_away_school = st.selectbox(
            "Away Team",
            away_options,
            index=(
                away_options.index(current_away_school)
                if current_away_school in away_options
                else 0
            ),
            key="schedule_new_away"
        )

        new_date = st.date_input(
            "Date",
            value=pd.to_datetime(selected_game["Date"]).date(),
            key="schedule_new_date"
        )

        new_week = st.number_input(
            "Week",
            min_value=1,
            max_value=15,
            value=int(selected_game["Week"]),
            step=1,
            key="schedule_new_week"
        )

        if st.button("Save Schedule Change", key="save_schedule_change"):

            new_home_id = team_options[new_home_school]
            new_away_id = team_options[new_away_school]

            if new_home_id == new_away_id:
                st.error("Home and away teams can't be the same.")
            else:
                new_division = teams.loc[
                    teams["TeamID"] == new_home_id,
                    "Division"
                ].values[0]

                supabase = get_supabase()

                supabase.table("games").update({
                    "Week": int(new_week),
                    "Date": new_date.isoformat(),
                    "HomeID": new_home_id,
                    "AwayID": new_away_id,
                    "Division": new_division
                }).eq(
                    "GameID",
                    selected_game_id
                ).execute()

                st.success(
                    f"Updated schedule: "
                    f"{new_home_school} vs {new_away_school}"
                )

                st.rerun()

        st.divider()

        st.markdown("### Delete Game")

        st.warning(
            "Deleting a game permanently removes it from the Supabase schedule."
        )

        confirm_delete = st.checkbox(
            "I understand that this will permanently delete the selected game.",
            key="confirm_delete_game"
        )

        if st.button(
            "Delete Game",
            key="delete_schedule_game",
            disabled=not confirm_delete
        ):
            supabase = get_supabase()

            supabase.table("games").delete().eq(
                "GameID",
                selected_game_id
            ).execute()

            st.success(
                f"Deleted {schedule_labels[selected_game_id]}"
            )

            st.rerun()

        
# ------------------------
# TAB 3: Graphics
# ------------------------
with tab4:
    st.subheader("Generate Weekly Graphic")

    rankings, season_started = get_rankings(games, teams)

    if not season_started:
        st.caption("Using Preseason Power Rankings — live MPI begins after Week 1.")

    class_filter = st.selectbox("Class", ["All", "A", "B"])

    display_rankings = rankings if class_filter == "All" else rankings[rankings["Class"] == class_filter]
    display_rankings = display_rankings.sort_values("MPI", ascending=False).reset_index(drop=True)
    display_rankings["Rank"] = display_rankings.index + 1

    subtitle = f"Class {class_filter}" if class_filter != "All" else ""
    title = "Preseason Rankings" if not season_started else "Weekly Rankings"

    if st.button("Generate Graphic", key="generate_ranking_graphic"):
        img = generate_ranking_graphic(display_rankings, title=title, subtitle=subtitle)
        buf = BytesIO()
        img.save(buf, format="PNG")
        st.image(img)
        st.download_button(
            "Download for Instagram", data=buf.getvalue(),
            file_name="maineyball_rankings.png", mime="image/png"
        )

with tab5:
    st.subheader("Generate Movers Graphic")

    movers = get_movers(games, teams)

    if movers is None:
        st.info("Movers graphic becomes available once Week 1 scores are entered.")
    else:
        st.caption(f"Change since {movers['baseline_label']}")

        if st.button("Generate Movers Graphic"):
            img = generate_movers_graphic(movers)
            buf = BytesIO()
            img.save(buf, format="PNG")

            st.image(img)
            st.download_button(
                "Download for Instagram", data=buf.getvalue(),
                file_name="maineyball_movers.png", mime="image/png"
            )

with tab6:  # add tab5 to your st.tabs(...) list, and import generate_quote_graphic
    st.subheader("Custom Text Graphic")
    headline = st.text_area("Headline", max_chars=100)
    subtext = st.text_area("Subtext (optional)", max_chars=250)

    if st.button("Generate Custom Graphic"):
        img = generate_quote_graphic(headline, subtext)
        buf = BytesIO()
        img.save(buf, format="PNG")
        st.image(img)
        st.download_button("Download for Instagram", data=buf.getvalue(),
                            file_name="maineyball_post.png", mime="image/png")

with tab7:
    st.subheader("Preseason Schedule Strength Index")
    st.caption("Ranks teams by the average preseason score of their in-conference opponents. Higher = harder road.")

    strength = compute_schedule_strength(games, teams)
    class_filter = st.selectbox("Class", ["All", "A", "B"], key="strength_class")

    display = strength if class_filter == "All" else strength[strength["Class"] == class_filter]
    display = display.sort_values("AvgOpponentScore", ascending=False).reset_index(drop=True)
    display["Rank"] = display.index + 1

    st.dataframe(display[["Rank", "Team", "AvgOpponentScore", "GamesCounted"]], hide_index=True)

    subtitle = f"Class {class_filter}" if class_filter != "All" else ""

    if st.button("Generate Graphic", key="generate_strength_graphic"):
        img = generate_schedule_strength_graphic(display, subtitle=subtitle)
        buf = BytesIO()
        img.save(buf, format="PNG")
        st.image(img)
        st.download_button("Download for Instagram", data=buf.getvalue(),
                            file_name="maineyball_strength.png", mime="image/png")

with tab8:
    st.subheader("Elo Rankings Graphic")

    elo_rankings = get_elo_rankings(games, teams)
    class_filter = st.selectbox("Class", ["All", "A", "B"], key="elo_class")

    display = elo_rankings if class_filter == "All" else elo_rankings[elo_rankings["Class"] == class_filter]
    display = display.sort_values("Elo", ascending=False).reset_index(drop=True)
    display["Rank"] = display.index + 1

    st.dataframe(display[["Rank", "Team", "Elo"]], hide_index=True)

    subtitle = f"Class {class_filter}" if class_filter != "All" else ""

    if st.button("Generate Graphic", key="generate_elo_graphic"):
        img = generate_ranking_graphic(display, title="Elo Rankings", subtitle=subtitle, value_col="Elo", decimals=0)
        buf = BytesIO()
        img.save(buf, format="PNG")
        st.image(img)
        st.download_button("Download for Instagram", data=buf.getvalue(),
                            file_name="maineyball_elo.png", mime="image/png", key="download_elo")
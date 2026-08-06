import pandas as pd
import streamlit as st

GAMES_COLUMNS = [
    "GameID", "Week", "Date", "HomeID", "AwayID",
    "Division", "Status", "HomeScore", "AwayScore"
]

def load_games(path="data/games.csv"):
    try:
        return pd.read_csv(path)
    except (pd.errors.EmptyDataError, FileNotFoundError):
        st.warning("No games scheduled yet — games.csv is empty or missing.")
        return pd.DataFrame(columns=GAMES_COLUMNS)

def load_teams(path="data/teams.csv"):
    try:
        return pd.read_csv(path)
    except (pd.errors.EmptyDataError, FileNotFoundError):
        st.error("teams.csv is missing or empty — can't load team data.")
        st.stop()
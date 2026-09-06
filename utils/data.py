import pandas as pd
import streamlit as st
from supabase import create_client

@st.cache_resource
def get_supabase():
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)

GAMES_COLUMNS = [
    "GameID", "Week", "Date", "HomeID", "AwayID",
    "Division", "Status", "HomeScore", "AwayScore"
]

def load_games():
    supabase = get_supabase()
    response = supabase.table("games").select("*").execute()
    return pd.DataFrame(response.data)

def load_teams(path="data/teams.csv"):
    try:
        return pd.read_csv(path)
    except (pd.errors.EmptyDataError, FileNotFoundError):
        st.error("teams.csv is missing or empty — can't load team data.")
        st.stop()
import pandas as pd
import streamlit as st
from supabase import create_client

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"],
)

games = pd.read_csv("data/games.csv")

for _, row in games.iterrows():

    home_score = (
        int(row["HomeScore"])
        if pd.notna(row["HomeScore"])
        else None
    )

    away_score = (
        int(row["AwayScore"])
        if pd.notna(row["AwayScore"])
        else None
    )

    game = {
        "GameID": row["GameID"],
        "Week": int(row["Week"]),
        "Date": str(row["Date"]),
        "HomeID": row["HomeID"],
        "AwayID": row["AwayID"],
        "OpponentName": (
            row["OpponentName"]
            if pd.notna(row["OpponentName"])
            else None
        ),
        "Division": row["Division"],
        "Status": row["Status"],
        "HomeScore": home_score,
        "AwayScore": away_score,
        "IsConference": bool(row["IsConference"]),
    }

    supabase.table("games").upsert(game).execute()

st.success(f"Successfully migrated {len(games)} games.")
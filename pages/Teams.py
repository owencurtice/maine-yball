
import streamlit as st
import pandas as pd

st.title("Teams")

teams = pd.read_csv("data/teams.csv")

division = st.selectbox(
    "Division",
    [
        "All",
        "A North",
        "A South",
        "B North",
        "B South"
    ]
)

if division != "All":
    teams = teams[teams["Division"] == division]

cols_per_row = 4
rows = [teams.iloc[i:i + cols_per_row] for i in range(0, len(teams), cols_per_row)]

for row in rows:
    cols = st.columns(cols_per_row)
    for col, (_, team) in zip(cols, row.iterrows()):
        with col:
            st.image(f"assets/logos/{team['Logo']}", width=100)
            st.markdown(f"**{team['School']}**")
            st.caption(f"{team['Mascot']} — {team['Class']} {team['Region']}")
            if st.button("View Team", key=f"team_{team['TeamID']}"):
                st.session_state["selected_team"] = team["TeamID"]
                st.switch_page("pages/_Team_Profile.py")
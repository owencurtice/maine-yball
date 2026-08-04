import streamlit as st


def team_profile(team):

    st.title(team["Team"])

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Record",
            f"{team['Wins']}-{team['Losses']}"
        )

    with c2:
        st.metric(
            "MPI",
            round(team["MPI"],1)
        )

    with c3:
        st.metric(
            "SOS",
            round(team["SOS"],3)
        )
import streamlit as st


def ranking_card(team):
    st.markdown(
        f"""<div class="card">
<div class="rank">#{team['Rank']}</div>
<div class="team">{team['Team']}</div>
<br>
Record: {team['Wins']}-{team['Losses']}
<br>
MPI: {team['MPI']:.1f}
</div>""",
        unsafe_allow_html=True
    )


def story_card(title, text):
    st.markdown(
        f"""<div class="card">
<h3>{title}</h3>
<p>{text}</p>
</div>""",
        unsafe_allow_html=True
    )


def prediction_card(team1, team2, prediction):
    st.markdown(
        f"""<div class="card">
<h3>{team1} vs {team2}</h3>
<h2>{prediction}%</h2>
</div>""",
        unsafe_allow_html=True
    )

import pandas as pd

def mpi_scorecard(row):
    data = [
        {
            "Metric": "Winning Percentage",
            "Score": f"{row['Winning_Percentage']:.3f}",
            "Weight": "40%",
            "Contribution": f"{row['Winning_Percentage'] * 0.40 * 100:.1f}"
        },
        {
            "Metric": "Strength of Schedule",
            "Score": f"{row['SOS']:.3f}",
            "Weight": "30%",
            "Contribution": f"{row['SOS'] * 0.30 * 100:.1f}"
        },
        {
            "Metric": "Offensive Rating",
            "Score": f"{row['Offensive_Rating']:.3f}",
            "Weight": "15%",
            "Contribution": f"{row['Offensive_Rating'] * 0.15 * 100:.1f}"
        },
        {
            "Metric": "Defensive Rating",
            "Score": f"{row['Defensive_Rating']:.3f}",
            "Weight": "15%",
            "Contribution": f"{row['Defensive_Rating'] * 0.15 * 100:.1f}"
        },
    ]
    df = pd.DataFrame(data)
    st.dataframe(df, hide_index=True, width="stretch")
    st.caption(f"MPI = Σ(Score × Weight) × 100 = **{row['MPI']:.1f}**")

def mover_card(team, delta, mpi):
    color = "#79983F" if delta >= 0 else "#B85C4A"
    arrow = "▲" if delta >= 0 else "▼"
    st.markdown(
        f"""<div class="card">
<div class="team">{team}</div>
<div style="color:{color};font-family:'Roboto Mono',monospace;font-size:28px;font-weight:700;">{arrow} {abs(delta):.1f}</div>
MPI: {mpi:.1f}
</div>""",
        unsafe_allow_html=True
    )
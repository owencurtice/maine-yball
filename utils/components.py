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
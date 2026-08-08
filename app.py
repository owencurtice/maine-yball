import streamlit as st
from pathlib import Path
from utils.components import story_card
from utils.theme import inject_theme
inject_theme()

# --------------------------
# PAGE CONFIG
# --------------------------
st.set_page_config(
    page_title="Maine-yball",
    page_icon="🏈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------
# THEME
# --------------------------
from utils.theme import inject_theme
inject_theme()

st.image(
    "assets/logo.png",
    width=180
)

st.title("MAINE-YBALL")

st.caption(
    "Revealing the true stories of Maine sports, beyond the logos, narratives, and noise."
)

st.write("""
Maine-yball is an independent football analytics publication
covering Maine Class A and Class B football.

Our goal is simple:
Use data, not reputation, to explain what is happening every Friday night.
""")

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Current Rankings")
    st.write("""
    Week to week team rankings based on the Maine-yball Power Index (MPI), 
    the metric allows us to evalute teams from class A and class B 
    and North vs South on a level playing field.
    """)

with col2:
    st.subheader("MPI")
    st.write("""
    The Maine-yball Power Index (MPI)
    is a comprehensive metric that evaluates Maine football teams based on
    winning percentage, strength of schedule,
    point differential, and offensive/defensive efficiency.
    """)

with col3:
    st.subheader("Elo and Predictions")
    st.write("""
    Elo ratings is an iterative system that updates a teams rating after every 
    game based on the result and the margin of victory, factoring in the opponents rating. 
    We use Elo to predict the outcome of future games.
    """)

st.image(
    "assets/featured.jpg",
    use_container_width=True
)
st.caption("""
Photo Credit: Insert Name; Insert Caption
""")

st.divider()

from utils.digest import load_digest, latest_entry

digest = load_digest()
latest = latest_entry(digest)

st.divider()

if latest is not None:
    story_card(f"Week {int(latest['Week'])}: {latest['Title']}", latest["Text"])
    if st.button("Read the Full Weekly Digest"):
        st.switch_page("pages/Weekly_Digest.py")
else:
    st.info("Weekly Digest coming soon.")

st.divider()

st.caption("""
Founded by Owen Curtice • Built with Python • Streamlit • Maine-yball Analytics
Covering Maine Class A & B Football
""")
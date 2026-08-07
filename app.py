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
    layout="wide"
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
    Week-by-week Maine-yball
    Power Index rankings for
    Class A & B football.
    """)

with col2:
    st.subheader("Game of the Week")
    st.write("""
    Weekly matchup analysis,
    predictions, and key metrics.
    """)

with col3:
    st.subheader("Weekly Digest")
    st.write("""
    Observations, trends,
    and stories hidden inside
    the numbers.
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
Built with Python • Streamlit • Maine-yball Analytics
Covering Maine Class A & B Football
""")
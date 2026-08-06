import streamlit as st
from utils.theme import inject_theme
from utils.digest import load_digest
from utils.components import story_card

inject_theme()

st.title("Weekly Digest")
st.caption("Observations, trends, and storylines from around the league.")

st.divider()

digest = load_digest()

if digest.empty:
    st.info("No digest entries yet. Check back soon.")
else:
    for _, entry in digest.sort_values("Week", ascending=False).iterrows():
        story_card(f"Week {int(entry['Week'])}: {entry['Title']}", entry["Text"])
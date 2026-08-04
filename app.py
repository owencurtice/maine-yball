import streamlit as st
import base64
from pathlib import Path
from utils.components import story_card

# --------------------------
# PAGE CONFIG
# --------------------------

st.set_page_config(
    page_title="Maine-yball",
    page_icon="🏈",
    layout="wide"
)

# --------------------------
# BACKGROUND
# --------------------------

def get_base64(image_path):
    with open(image_path, "rb") as image:
        return base64.b64encode(image.read()).decode()

background = get_base64("assets/background.jpg")

css = Path("styles/main.css").read_text()

st.markdown(
    f"<style>{css}</style>",
    unsafe_allow_html=True
)
st.image(
    "assets/logo.png",
    width=180
)

st.title("MAINE-YBALL")

st.image(

    "assets/featured.jpg",

    use_container_width=True

)

st.caption(
    "Revealing the true stories of Maine sports, beyond the logos, narratives, and noise."
)

st.write("""
Maine-yball is an independent football analytics publication
covering Maine Class A and Class B football.

Our goal is simple:

Use data—not reputation—to explain what is happening every Friday night.
""")

st.divider()

col1,col2,col3 = st.columns(3)

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

    st.subheader("Notebook")

    st.write("""
Observations, trends,
and stories hidden inside
the numbers.
""")

st.image(
    "assets/background.jpg",
    use_container_width=True
)

st.divider()

story_card(

    "Notebook",

    "Every ranking tells a story. This week, Thornton Academy's rise wasn't just about winning—it was about who they beat."

)

st.divider()

story_card(

    "Featured Analysis",

    "Why Bonny Eagle deserves to be ranked higher than their record suggests."

)

st.divider()
st.caption(
"""
Built with Python • Streamlit • Maine-yball Analytics

Covering Maine Class A & Class B Football
"""
)

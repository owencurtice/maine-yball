import streamlit as st
import base64
import pandas as pd
from models.mpi import calculate_mpi

# Page settings (must be first Streamlit command)
st.set_page_config(
    page_title="Maine-yball",
    page_icon="🏈",
    layout="wide"
)


# Convert image to base64
def get_base64(image_path):
    with open(image_path, "rb") as image:
        return base64.b64encode(image.read()).decode()


background = get_base64("assets/background.jpg")


# Maine-yball Theme
st.markdown(
    f"""
    <style>

    .stApp {{
        background:
        linear-gradient(
            rgba(0,0,0,0.80),
            rgba(0,0,0,0.90)
        ),
        url("data:image/jpeg;base64,{background}");

        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}


    h1 {{
        color: white;
        font-size: 55px;
        font-weight: 900;
        letter-spacing: 2px;
    }}


    h2 {{
        color: #d9d9d9;
    }}


    p {{
        color: #eeeeee;
    }}

    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar
page = st.sidebar.selectbox(
    "Navigate",
    [
        "Home",
        "Football Analytics",
        "Team Comparison",
        "About MPI",
        "Hockey Analytics",
        "Data Lab"
    ]
)


# HOME
if page == "Home":

    st.title("MAINE-YBALL")

    st.caption(
        "Revealing the true stories of Maine sports, beyond the logos, narratives, and noise."
    )

    st.subheader(
        "Where data uncovers the stories behind Maine athletics."
    )

    st.write(
        """
        Maine-yball is a sports analytics platform built to uncover
        the hidden insights behind Maine athletics.

        Using statistics, visualization, and predictive modeling,
        Maine-yball evaluates teams beyond reputation and traditional rankings.
        """
    )


    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Sports Covered",
            "2"
        )

    with col2:
        st.metric(
            "Analytics Models",
            "1"
        )

    with col3:
        st.metric(
            "Built With",
            "Python"
        )


elif page == "Football Analytics":

    st.title("🏈 Football Intelligence Center")


    df = pd.read_csv(
        "data/football_stats.csv"
    )


    df = calculate_mpi(df)


    rankings = df.sort_values(
        "MPI",
        ascending=False
    )


    st.header("🏆 Maine-yball Power Index")


    st.dataframe(
        rankings[
            [
                "Team",
                "Wins",
                "Losses",
                "MPI"
            ]
        ]
    )


    st.header("📊 MPI Rankings")


    st.bar_chart(
        rankings,
        x="Team",
        y="MPI"
    )


# COMPARISON
elif page == "Team Comparison":

    st.title("Team Comparison")

    st.write(
        "Compare Maine teams using advanced analytics."
    )


# MPI
elif page == "About MPI":

    st.title("Maine-yball Power Index")

    st.write(
        """
        The Maine-yball Power Index evaluates teams beyond
        traditional wins and losses.

        MPI will consider:

        • Winning percentage
        • Strength of schedule
        • Quality wins
        • Predictive analytics
        """
    )


# HOCKEY
elif page == "Hockey Analytics":

    st.title("Hockey Intelligence Center")

    st.write(
        """
        Coming Winter:

        Maine hockey analytics,
        rankings, and predictions.
        """
    )


# LAB
elif page == "Data Lab":

    st.title("Maine-yball Data Lab")

    st.write(
        """
        Experimental models, statistics,
        and machine learning projects.
        """
    )
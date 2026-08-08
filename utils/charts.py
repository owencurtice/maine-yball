import streamlit as st
import altair as alt


def mpi_chart(df):
    chart = (
        alt.Chart(df)
        .mark_bar(color="#79983F")
        .encode(
            x=alt.X("MPI:Q", title="MPI"),
            y=alt.Y("Team:N", sort="-x", title=None),
            tooltip=["Team", "MPI"]
        )
        .properties(height=alt.Step(35))
    )
    st.altair_chart(chart, width="stretch")


def offense_defense_quadrant(df):
    base = alt.Chart(df).encode(
        x=alt.X("Offensive_Rating:Q", title="Offensive Rating", scale=alt.Scale(domain=[0, 1])),
        y=alt.Y("Defensive_Rating:Q", title="Defensive Rating", scale=alt.Scale(domain=[0, 1])),
        tooltip=["Team", "Offensive_Rating", "Defensive_Rating"]
    )

    points = base.mark_circle(size=120, color="#79983F")
    labels = base.mark_text(align="left", dx=7, dy=-3, color="#F2F1EC").encode(text="Team")

    mid_x = alt.Chart(df).mark_rule(color="gray", strokeDash=[4, 4]).encode(x=alt.datum(0.5))
    mid_y = alt.Chart(df).mark_rule(color="gray", strokeDash=[4, 4]).encode(y=alt.datum(0.5))

    chart = (mid_x + mid_y + points + labels).properties(height=500)
    st.altair_chart(chart, width="stretch")

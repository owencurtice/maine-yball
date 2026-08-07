import streamlit as st
from utils.theme import inject_theme

inject_theme()

st.title("About Maine-yball")

st.write(
"""
Maine-yball is a student-created data-driven platform for analyzing Maine football 
teams beyond the tradiional wins and losses and brand recognition. Our goal is to
provide a more accurate and comprehensive evaluation of Maine football teams through advanced metrics, 
predictive analytics, and evidence-based analysis. This platform is ever-evolving and will continue 
to be updated with new features, data, and insights as we work to provide the most accurate and 
comprehensive evaluation of Maine football teams.
"""
)

st.divider()

st.title("MPI Explained")

st.write(
"""
The Maine-yball Power Index (MPI) is a comprehensive metric that evaluates Maine football teams beyond 
traditional wins and losses. It takes into account various factors such as winning percentage, strength 
of schedule, point differential, and offensive/defensive efficiency to provide a more accurate assessment
of team performance.
"""
)

st.divider()

st.title("Rankings and Analysis updated every Sunday!")
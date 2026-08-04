import streamlit as st


def mpi_chart(rankings):

    st.bar_chart(

        rankings,

        x="Team",

        y="MPI"

    )
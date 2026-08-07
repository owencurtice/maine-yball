import streamlit as st
from pathlib import Path

def inject_theme():
    css = Path("styles/main.css").read_text()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
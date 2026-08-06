import streamlit as st

def require_admin_password():
    if st.session_state.get("is_admin"):
        return

    password = st.text_input("Admin Password", type="password")

    if password:
        if password == st.secrets["admin_password"]:
            st.session_state["is_admin"] = True
            st.rerun()
        else:
            st.error("Incorrect password.")
            st.stop()
    else:
        st.stop()
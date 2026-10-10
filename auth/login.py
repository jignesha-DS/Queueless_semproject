import streamlit as st
import pandas as pd
from datetime import datetime, date, time, timedelta
from database import get_connection
from utils.functions import *

def login_page():

    st.title("🔐 Login")

    login_type = st.radio(
        "Login as",
        ["Patient", "Doctor", "Admin"],
        horizontal=True,
        key="login_type"
    )

    email = st.text_input(
        "Email",
        key="login_email"
    )

    password = st.text_input(
        "Password",
        type="password",
        key="login_password"
    )

    if st.button(
        "Login",
        use_container_width=True,
        key="login_button"
    ):

        if not email or not password:
            st.error("Please enter email and password.")
            return

        result = execute_query(
            """
            SELECT *
            FROM users
            WHERE email = %s
            AND password = %s
            """,
            (email, password),
            fetch=True
        )

        if not result:
            st.error("Invalid email or password.")
            return

        user = result[0]

        selected_role = login_type.lower()

        if user["role"] != selected_role:
            st.error(
                f"This account is registered as {user['role'].title()}."
            )
            return

        st.session_state.logged_in = True
        st.session_state.user_id = user["id"]
        st.session_state.name = user["name"]
        st.session_state.role = user["role"]
        st.session_state.email = user["email"]

        st.success("Login successful!")
        st.rerun()

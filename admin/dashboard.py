import streamlit as st
import pandas as pd
from datetime import datetime, date, time, timedelta
from database import get_connection
from utils.functions import *

def admin_dashboard():

    st.title("🛡️ Admin Dashboard")

    users = execute_query(
        """
        SELECT *
        FROM users
        ORDER BY id DESC
        """,
        fetch=True
    ) or []

    doctors = get_doctors()

    patients = execute_query(
        """
        SELECT
            p.*,
            u.name,
            u.email,
            u.phone
        FROM patients p
        JOIN users u ON p.user_id = u.id
        ORDER BY p.patient_id DESC
        """,
        fetch=True
    ) or []

    today_tokens = execute_query(
        """
        SELECT *
        FROM tokens
        WHERE queue_date = CURDATE()
        """,
        fetch=True
    ) or []

    total_users = len(users)

    total_doctors = len(doctors)

    total_patients = len(patients)

    total_tokens = len(today_tokens)

    completed = len([
        t for t in today_tokens
        if t["status"] == "COMPLETED"
    ])

    waiting = len([
        t for t in today_tokens
        if t["status"] == "WAITING"
    ])

    cancelled = len([
        t for t in today_tokens
        if t["status"] == "CANCELLED"
    ])

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Users",
            total_users
        )

    with col2:
        st.metric(
            "Doctors",
            total_doctors
        )

    with col3:
        st.metric(
            "Patients",
            total_patients
        )

    with col4:
        st.metric(
            "Today's Tokens",
            total_tokens
        )

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Completed",
            completed
        )

    with col2:
        st.metric(
            "Waiting",
            waiting
        )

    with col3:
        st.metric(
            "Cancelled",
            cancelled
        )

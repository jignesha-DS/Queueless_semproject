import streamlit as st
import pandas as pd
from datetime import datetime, date, time, timedelta
from database import get_connection
from utils.functions import *

def patient_dashboard():

    st.title(f"👋 Welcome, {st.session_state.name}")

    patient = get_patient()

    if not patient:
        st.error("Patient profile not found.")
        return

    active_token = get_patient_token(
        patient["patient_id"]
    )

    if active_token:

        people_ahead = get_people_ahead(
            active_token["doctor_id"],
            active_token["token_number"]
        )

        estimated_wait = (
            people_ahead *
            active_token["average_time"]
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "My Token",
                f"A-{active_token['token_number']:02d}"
            )

        with col2:
            st.metric(
                "People Ahead",
                people_ahead
            )

        with col3:
            st.metric(
                "Estimated Wait",
                f"{estimated_wait} min"
            )

        st.info(
            f"Doctor: Dr. {active_token['doctor_name']} | "
            f"Status: {active_token['status']}"
        )

    else:

        st.info(
            "You don't have an active token. "
            "Go to Book Token to join a queue."
        )

    notifications = get_notifications(
        st.session_state.user_id
    )

    unread = [
        n for n in notifications
        if not n["is_read"]
    ]

    if unread:

        st.warning(
            f"🔔 You have {len(unread)} unread notification(s)."
        )

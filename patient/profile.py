import streamlit as st
import pandas as pd
from datetime import datetime, date, time, timedelta
from database import get_connection
from utils.functions import *

def patient_profile():

    patient = get_patient()

    if not patient:
        st.error("Patient profile not found.")
        return

    st.title("👤 My Profile")

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Personal Information")

        st.write(
            f"**Name:** {st.session_state.name}"
        )

        st.write(
            f"**Email:** {st.session_state.email}"
        )

        st.write(
            f"**Age:** {patient.get('age', '-')}"
        )

        st.write(
            f"**Gender:** {patient.get('gender', '-')}"
        )

    with col2:

        st.subheader("Contact Information")

        st.write(
            f"**Phone:** {patient.get('phone', '-')}"
        )

        st.write(
            f"**Address:** {patient.get('address', '-')}"
        )

        st.write(
            f"**Emergency Contact:** "
            f"{patient.get('emergency_contact', '-')}"
        )

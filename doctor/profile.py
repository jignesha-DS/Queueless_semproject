import streamlit as st
import pandas as pd
from datetime import datetime, date, time, timedelta
from database import get_connection
from utils.functions import *

def doctor_profile():

    doctor = get_doctor()

    if not doctor:
        st.error("Doctor profile not found.")
        return

    st.title("👨‍⚕️ Doctor Profile")

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Personal Information")

        st.write(
            f"**Name:** Dr. {doctor['name']}"
        )

        st.write(
            f"**Email:** {doctor['email']}"
        )

        st.write(
            f"**Phone:** {doctor.get('phone', '-')}"
        )

        st.write(
            f"**Address:** {doctor.get('address', '-')}"
        )

    with col2:

        st.subheader("Professional Information")

        st.write(
            f"**Specialization:** "
            f"{doctor.get('specialization', '-')}"
        )

        st.write(
            f"**Degree:** "
            f"{doctor.get('degree', '-')}"
        )

        st.write(
            f"**Experience:** "
            f"{doctor.get('experience', 0)} years"
        )

        st.write(
            f"**Consultation Fees:** "
            f"₹{doctor.get('fees', 0)}"
        )

        st.write(
            f"**Room:** "
            f"{doctor.get('room_no', '-')}"
        )

        st.write(
            f"**Average Time:** "
            f"{doctor.get('average_time', 10)} minutes"
        )

        st.write(
            f"**Availability:** "
            f"{doctor.get('availability', 'Available')}"
        )

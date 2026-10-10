import streamlit as st
import pandas as pd
from datetime import datetime, date, time, timedelta
from database import get_connection
from utils.functions import *

def doctor_availability():

    doctor = get_doctor()

    if not doctor:
        return

    st.title("🟢 Availability")

    current_status = doctor.get(
        "availability",
        "Available"
    )

    st.write(
        f"Current status: **{current_status}**"
    )

    new_status = st.selectbox(
        "Set Availability",
        [
            "Available",
            "Busy",
            "On Break",
            "Unavailable"
        ],
        index=[
            "Available",
            "Busy",
            "On Break",
            "Unavailable"
        ].index(current_status)
        if current_status in
        ["Available", "Busy", "On Break", "Unavailable"]
        else 0,
        key="doctor_availability_select"
    )

    if st.button(
        "Update Availability",
        key="update_availability"
    ):

        result = execute_query(
            """
            UPDATE doctors
            SET availability = %s
            WHERE doctor_id = %s
            """,
            (
                new_status,
                doctor["doctor_id"]
            )
        )

        if result:

            st.success(
                "Availability updated successfully."
            )

            st.rerun()

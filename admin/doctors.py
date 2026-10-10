import streamlit as st
import pandas as pd
from datetime import datetime, date, time, timedelta
from database import get_connection
from utils.functions import *

def admin_doctors():

    st.title("👨‍⚕️ Manage Doctors")

    doctors = get_doctors()

    if not doctors:

        st.info("No doctors found.")
        return

    df = pd.DataFrame(doctors)

    columns = [
        "name",
        "email",
        "specialization",
        "degree",
        "fees",
        "experience",
        "room_no",
        "availability"
    ]

    st.dataframe(
        df[columns],
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader("Update Doctor Availability")

    doctor_names = {}

    for doctor in doctors:

        label = (
            f"Dr. {doctor['name']} - "
            f"{doctor['specialization']}"
        )

        doctor_names[label] = doctor

    selected = st.selectbox(
        "Select Doctor",
        list(doctor_names.keys()),
        key="admin_doctor_select"
    )

    doctor = doctor_names[selected]

    new_status = st.selectbox(
        "New Status",
        [
            "Available",
            "Busy",
            "On Break",
            "Unavailable"
        ],
        key="admin_doctor_status"
    )

    if st.button(
        "Update Doctor",
        key="admin_update_doctor"
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
                "Doctor status updated."
            )

            st.rerun()

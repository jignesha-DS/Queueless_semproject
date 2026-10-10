import streamlit as st
import pandas as pd
from datetime import datetime, date, time, timedelta
from database import get_connection
from utils.functions import *

def doctor_dashboard():

    doctor = get_doctor()

    if not doctor:
        st.error("Doctor profile not found.")
        return

    st.title(
        f"👨‍⚕️ Dr. {doctor['name']}"
    )

    queue = get_doctor_queue(
        doctor["doctor_id"]
    )

    waiting = len([
        x for x in queue
        if x["status"] == "WAITING"
    ])

    in_progress = len([
        x for x in queue
        if x["status"] == "IN_PROGRESS"
    ])

    completed = len([
        x for x in queue
        if x["status"] == "COMPLETED"
    ])

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Patients",
            len(queue)
        )

    with col2:
        st.metric(
            "Waiting",
            waiting
        )

    with col3:
        st.metric(
            "In Progress",
            in_progress
        )

    with col4:
        st.metric(
            "Completed",
            completed
        )

    st.divider()

    current = get_current_token(
        doctor["doctor_id"]
    )

    if current:

        st.success(
            f"Current: A-{current['token_number']:02d} "
            f"- {current['patient_name']} "
            f"- {current['status']}"
        )

    else:

        st.info("No patient currently being served.")

    st.subheader("Today's Queue")

    if queue:

        df = pd.DataFrame(queue)

        columns = [
            "token_number",
            "patient_name",
            "age",
            "gender",
            "status"
        ]

        st.dataframe(
            df[columns],
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No patients today.")

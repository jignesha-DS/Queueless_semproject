import streamlit as st
import pandas as pd
from datetime import datetime, date, time, timedelta
from database import get_connection
from utils.functions import *

def patient_book_token():

    patient = get_patient()

    if not patient:
        st.error("Patient profile not found.")
        return

    st.title("🎫 Book Token")

    active_token = get_patient_token(patient["patient_id"])

    if active_token:

        st.warning(
            f"You already have an active token: "
            f"A-{active_token['token_number']:02d}"
        )

        st.info(
            f"Doctor: Dr. {active_token['doctor_name']} | "
            f"Status: {active_token['status']}"
        )

        return

    doctors = get_doctors()

    if not doctors:
        st.warning("No doctors are registered.")
        return

    doctor_options = {}

    for doctor in doctors:

        label = (
            f"Dr. {doctor['name']} | "
            f"{doctor['specialization']} | "
            f"₹{doctor['fees']}"
        )

        doctor_options[label] = doctor

    selected_label = st.selectbox(
        "Select Doctor",
        list(doctor_options.keys()),
        key="book_doctor_select"
    )

    doctor = doctor_options[selected_label]

    st.markdown(
        f"""
        <div class="card">
        <h3>Dr. {doctor['name']}</h3>
        <p><b>Specialization:</b> {doctor['specialization']}</p>
        <p><b>Degree:</b> {doctor['degree']}</p>
        <p><b>Experience:</b> {doctor['experience']} years</p>
        <p><b>Consultation Fees:</b> ₹{doctor['fees']}</p>
        <p><b>Room:</b> {doctor['room_no']}</p>
        <p><b>Average Consultation:</b> {doctor['average_time']} minutes</p>
        <p><b>Status:</b> {doctor['availability']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if doctor["availability"] != "Available":
        st.warning("This doctor is currently unavailable.")
        return

    if st.button(
        "🎫 Generate Token",
        use_container_width=True,
        key="generate_token_button"
    ):

        token_number = get_next_token_number(
            doctor["doctor_id"]
        )

        token_id = execute_query(
            """
            INSERT INTO tokens
            (
                patient_id,
                doctor_id,
                token_number,
                queue_date,
                status
            )
            VALUES (%s, %s, %s, CURDATE(), 'WAITING')
            """,
            (
                patient["patient_id"],
                doctor["doctor_id"],
                token_number
            )
        )

        if token_id:

            user_result = execute_query(
                """
                SELECT user_id
                FROM doctors
                WHERE doctor_id = %s
                """,
                (doctor["doctor_id"],),
                fetch=True
            )

            if user_result:
                create_notification(
                    user_result[0]["user_id"],
                    f"New patient token A-{token_number:02d} "
                    f"has been generated.",
                    "NEW_TOKEN"
                )

            st.success(
                f"🎫 Your token is A-{token_number:02d}"
            )

            st.info(
                "Please monitor the Live Queue for your turn."
            )

            st.rerun()

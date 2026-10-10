import streamlit as st
import pandas as pd
from datetime import datetime, date, time, timedelta
from database import get_connection
from utils.functions import *

def patient_appointments():

    patient = get_patient()

    if not patient:
        return

    st.title("📅 Appointments")

    st.subheader("Book Appointment")

    doctors = get_doctors()

    if not doctors:
        st.info("No doctors available.")
        return

    doctor_options = {}

    for doctor in doctors:

        label = (
            f"Dr. {doctor['name']} - "
            f"{doctor['specialization']}"
        )

        doctor_options[label] = doctor

    selected = st.selectbox(
        "Select Doctor",
        list(doctor_options.keys()),
        key="appointment_doctor"
    )

    doctor = doctor_options[selected]
    
    # Display selected doctor's details
    st.subheader("👨‍⚕️ Doctor Details")

    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**Name:** Dr. {doctor['name']}")
        st.write(f"**Specialization:** {doctor['specialization']}")
        st.write(f"**Room Number:** {doctor.get('room_no', 'Not available')}")
        st.write(f"**Experience:** {doctor.get('experience', 'Not available')} years")

    with col2:
        st.write(f"**Consultation Time:** {doctor.get('average_time', 'Not available')} minutes")
        st.write(f"**Consultation Fees:** ₹{doctor.get('fees', 'Not available')}")
        st.write(f"**Availability:** {doctor.get('availability', 'Available')}")

    st.divider()


    appointment_date = st.date_input(
        "Appointment Date",
        min_value=date.today(),
        key="appointment_date"
    )

    appointment_time = st.time_input(
        "Appointment Time",
        value=time(10, 0),
        key="appointment_time"
    )

    if st.button(
        "Book Appointment",
        key="book_appointment_button"
    ):

        appointment_id = execute_query(
            """
            INSERT INTO appointments
            (
                patient_id,
                doctor_id,
                appointment_date,
                appointment_time,
                status
            )
            VALUES (%s, %s, %s, %s, 'BOOKED')
            """,
            (
                patient["patient_id"],
                doctor["doctor_id"],
                appointment_date,
                appointment_time
            )
        )

        if appointment_id:

            st.success(
                "✅ Appointment booked successfully."
            )

    st.divider()

    st.subheader("My Appointments")

    appointments = execute_query(
        """
        SELECT
            a.*,
            u.name AS doctor_name,
            d.specialization
        FROM appointments a
        JOIN doctors d ON a.doctor_id = d.doctor_id
        JOIN users u ON d.user_id = u.id
        WHERE a.patient_id = %s
        ORDER BY a.appointment_date DESC,
                 a.appointment_time DESC
        """,
        (patient["patient_id"],),
        fetch=True
    ) or []

    if appointments:

        df = pd.DataFrame(appointments)

        columns = [
            "appointment_date",
            "appointment_time",
            "doctor_name",
            "specialization",
            "status"
        ]

        st.dataframe(
            df[columns],
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No appointments found.")

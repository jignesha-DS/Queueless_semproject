import streamlit as st
import pandas as pd
from datetime import datetime, date, time, timedelta
from database import get_connection
from utils.functions import *

def patient_registration():

    st.title("👤 Patient Registration")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input(
            "Full Name",
            key="patient_reg_name"
        )

        email = st.text_input(
            "Email",
            key="patient_reg_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="patient_reg_password"
        )

        phone = st.text_input(
            "Phone Number",
            key="patient_reg_phone"
        )

    with col2:
        age = st.number_input(
            "Age",
            min_value=1,
            max_value=120,
            value=18,
            key="patient_reg_age"
        )

        gender = st.selectbox(
            "Gender",
            ["Male", "Female", "Other"],
            key="patient_reg_gender"
        )

        address = st.text_area(
            "Address",
            key="patient_reg_address"
        )

        emergency_contact = st.text_input(
            "Emergency Contact",
            key="patient_reg_emergency"
        )
    if st.button(
        "Register Patient",
        use_container_width=True,
        key="patient_register_button"
    ):

        if not name or not email or not password:
            st.error("Please fill Name, Email and Password.")
            return

        if not address:
            st.error("Please enter your address.")
            return

        existing = execute_query(
            """
            SELECT id
            FROM users
            WHERE email = %s
            """,
            (email,),
            fetch=True
        )

        if existing:
            st.error("Email is already registered.")
            return

        conn = None
        cursor = None

        try:

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO users
                (name, email, password, role, phone)
                VALUES (%s, %s, %s, 'patient', %s)
                """,
                (name, email, password, phone)
            )

            user_id = cursor.lastrowid

            cursor.execute(
                """
                INSERT INTO patients
                (user_id, age, gender, address, emergency_contact)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    user_id,
                    age,
                    gender,
                    address,
                    emergency_contact
                )
            )

            conn.commit()

            st.success(
                "✅ Patient registration successful! "
                "You can now login."
            )

        except Exception as e:

            if conn:
                conn.rollback()

            st.error(f"Registration failed: {e}")

        finally:

            if cursor:
                cursor.close()

            if conn:
                conn.close()

def doctor_registration():

    st.title("👨‍⚕️ Doctor Registration")

    st.info(
        "Create your professional doctor profile to manage "
        "patients and hospital queues."
    )

    st.subheader("Personal Information")

    col1, col2 = st.columns(2)

    with col1:

        name = st.text_input(
            "Doctor Name",
            key="doctor_reg_name"
        )

        email = st.text_input(
            "Email",
            key="doctor_reg_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="doctor_reg_password"
        )

        phone = st.text_input(
            "Phone Number",
            key="doctor_reg_phone"
        )

    with col2:

        address = st.text_area(
            "Address",
            key="doctor_reg_address"
        )

    st.subheader("Professional Information")

    col1, col2 = st.columns(2)

    with col1:

        specialization = st.text_input(
            "Specialization",
            placeholder="Example: Cardiologist",
            key="doctor_reg_specialization"
        )

        degree = st.text_input(
            "Degree",
            placeholder="Example: MBBS, MD",
            key="doctor_reg_degree"
        )

        fees = st.number_input(
            "Consultation Fees (₹)",
            min_value=0.0,
            step=50.0,
            key="doctor_reg_fees"
        )

    with col2:

        experience = st.number_input(
            "Years of Experience",
            min_value=0,
            max_value=60,
            value=0,
            step=1,
            key="doctor_reg_experience"
        )

        room_no = st.text_input(
            "Room Number",
            placeholder="Example: Room 2",
            key="doctor_reg_room"
        )

        average_time = st.number_input(
            "Average Consultation Time (minutes)",
            min_value=1,
            max_value=120,
            value=10,
            key="doctor_reg_avg_time"
        )

    if st.button(
        "Register Doctor",
        use_container_width=True,
        key="doctor_register_button"
    ):

        if not name or not email or not password:
            st.error("Please fill Name, Email and Password.")
            return

        if not specialization or not degree:
            st.error("Please enter Specialization and Degree.")
            return

        if not address:
            st.error("Please enter Address.")
            return

        existing = execute_query(
            """
            SELECT id
            FROM users
            WHERE email = %s
            """,
            (email,),
            fetch=True
        )

        if existing:
            st.error("Email is already registered.")
            return

        conn = None
        cursor = None

        try:

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO users
                (name, email, password, role, phone)
                VALUES (%s, %s, %s, 'doctor', %s)
                """,
                (
                    name,
                    email,
                    password,
                    phone
                )
            )

            user_id = cursor.lastrowid

            cursor.execute(
                """
                INSERT INTO doctors
                (
                    user_id,
                    specialization,
                    room_no,
                    average_time,
                    availability,
                    experience,
                    degree,
                    fees,
                    address
                )
                VALUES
                (
                    %s, %s, %s, %s, 'Available',
                    %s, %s, %s, %s
                )
                """,
                (
                    user_id,
                    specialization,
                    room_no,
                    average_time,
                    experience,
                    degree,
                    fees,
                    address
                )
            )

            conn.commit()

            st.success(
                "✅ Doctor registration successful! "
                "You can now login."
            )

        except Exception as e:

            if conn:
                conn.rollback()

            st.error(f"Registration failed: {e}")

        finally:

            if cursor:
                cursor.close()

            if conn:
                conn.close()

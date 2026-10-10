import streamlit as st
import pandas as pd
from datetime import datetime, date, time, timedelta

from utils.functions import logout
from auth.login import login_page
from auth.register import patient_registration, doctor_registration
from patient.dashboard import patient_dashboard
from patient.token import patient_book_token
from patient.queue import patient_live_queue
from patient.notifications import patient_notifications
from patient.history import patient_history
from patient.appointments import patient_appointments
from patient.profile import patient_profile
from doctor.dashboard import doctor_dashboard
from doctor.queue import doctor_queue
from doctor.profile import doctor_profile
from doctor.availability import doctor_availability
from doctor.doctor_break import doctor_break
from doctor.notifications import doctor_notifications
from admin.dashboard import admin_dashboard
from admin.doctors import admin_doctors
from admin.patients import admin_patients
from admin.users import admin_users
from admin.queue import admin_queue
from admin.analytics import admin_analytics
from admin.notifications import admin_notifications
from admin.appointments import admin_appointments

st.set_page_config(page_title="QueueLess", page_icon="🏥", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
.main-title {font-size:38px;font-weight:700;margin-bottom:5px;}
.subtitle {font-size:18px;color:#666;margin-bottom:25px;}
.card {padding:20px;border-radius:12px;background-color:#f7f9fc;border:1px solid #e5e7eb;margin-bottom:15px;}
.token-box {padding:25px;border-radius:15px;text-align:center;background-color:#eef6ff;border:2px solid #d6e9ff;}
.token-number {font-size:45px;font-weight:bold;}
.stat-box {padding:20px;border-radius:12px;background-color:#f7f7f7;text-align:center;border:1px solid #ddd;}
.small-text {color:#666;font-size:14px;}
</style>
""", unsafe_allow_html=True)

def home_page():

    st.markdown(
        '<div class="main-title">🏥 QueueLess</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Smart Hospital Queue & Patient Waiting-Time Management System</div>',
        unsafe_allow_html=True
    )

    st.write(
        "QueueLess helps patients avoid unnecessary waiting and helps "
        "doctors and hospitals manage queues efficiently."
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="card">
            <h3>🎫 Smart Token</h3>
            <p>Generate a digital token without standing in a long queue.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div class="card">
            <h3>⏱️ Live Waiting Time</h3>
            <p>Know your position and estimated waiting time.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            """
            <div class="card">
            <h3>🔔 Notifications</h3>
            <p>Receive updates when your token is called.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    st.subheader("How QueueLess Works")

    step1, step2, step3, step4 = st.columns(4)

    with step1:
        st.info("1️⃣ Register\n\nCreate your account.")

    with step2:
        st.info("2️⃣ Select Doctor\n\nChoose a doctor.")

    with step3:
        st.info("3️⃣ Get Token\n\nGenerate your queue token.")

    with step4:
        st.info("4️⃣ Track Queue\n\nMonitor your waiting time.")

def initialize_session():
    defaults = {"logged_in": False, "user_id": None, "name": None, "role": None, "email": None}
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

initialize_session()

def admin_page():

    menu = st.selectbox(
        "Admin Section",
        [
            "Dashboard",
            "Doctors",
            "Patients",
            "Users",
            "Queue Monitoring",
            "Appointments",
            "Analytics",
            "Notifications"
        ],
        key="admin_section"
    )

    if menu == "Dashboard":
        admin_dashboard()

    elif menu == "Doctors":
        admin_doctors()

    elif menu == "Patients":
        admin_patients()

    elif menu == "Users":
        admin_users()

    elif menu == "Queue Monitoring":
        admin_queue()

    elif menu == "Appointments":
        admin_appointments()

    elif menu == "Analytics":
        admin_analytics()

    elif menu == "Notifications":
        admin_notifications()

def patient_page():

    menu = st.selectbox(
        "Patient Section",
        [
            "Dashboard",
            "Book Token",
            "Live Queue",
            "Notifications",
            "Token History",
            "Appointments",
            "My Profile"
        ],
        key="patient_section"
    )

    if menu == "Dashboard":
        patient_dashboard()

    elif menu == "Book Token":
        patient_book_token()

    elif menu == "Live Queue":
        patient_live_queue()

    elif menu == "Notifications":
        patient_notifications()

    elif menu == "Token History":
        patient_history()

    elif menu == "Appointments":
        patient_appointments()

    elif menu == "My Profile":
        patient_profile()

def doctor_page():

    menu = st.selectbox(
        "Doctor Section",
        [
            "Dashboard",
            "Today's Queue",
            "My Profile",
            "Availability",
            "Break",
            "Notifications"
        ],
        key="doctor_section"
    )

    if menu == "Dashboard":
        doctor_dashboard()

    elif menu == "Today's Queue":
        doctor_queue()

    elif menu == "My Profile":
        doctor_profile()

    elif menu == "Availability":
        doctor_availability()

    elif menu == "Break":
        doctor_break()

    elif menu == "Notifications":
        doctor_notifications()

def logged_in_app():

    st.sidebar.success(
        f"Logged in as {st.session_state.name}"
    )

    st.sidebar.write(
        f"Role: {st.session_state.role.title()}"
    )

    if st.sidebar.button(
        "🚪 Logout",
        use_container_width=True,
        key="logout_button"
    ):

        logout()

    st.sidebar.divider()

    if st.session_state.role == "patient":

        patient_page()

    elif st.session_state.role == "doctor":

        doctor_page()

    elif st.session_state.role == "admin":

        admin_page()

def main():
    if st.session_state.logged_in:
        logged_in_app()
    else:
        st.sidebar.title("🏥 QueueLess")
        menu = st.sidebar.radio(
            "Menu",
            ["Home", "Login", "Patient Registration", "Doctor Registration"],
            key="main_menu"
        )
        if menu == "Home":
            home_page()
        elif menu == "Login":
            login_page()
        elif menu == "Patient Registration":
            patient_registration()
        elif menu == "Doctor Registration":
            doctor_registration()

if __name__ == "__main__":
    main()

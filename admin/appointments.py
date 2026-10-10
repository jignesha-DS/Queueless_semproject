import streamlit as st
import pandas as pd
from datetime import datetime, date, time, timedelta
from database import get_connection
from utils.functions import *

def admin_appointments():

    st.title("📅 Appointment Management")

    appointments = execute_query(
        """
        SELECT
            a.appointment_id,
            a.appointment_date,
            a.appointment_time,
            a.status,
            pu.name AS patient_name,
            du.name AS doctor_name,
            d.specialization
        FROM appointments a
        JOIN patients p
            ON a.patient_id = p.patient_id
        JOIN users pu
            ON p.user_id = pu.id
        JOIN doctors d
            ON a.doctor_id = d.doctor_id
        JOIN users du
            ON d.user_id = du.id
        ORDER BY
            a.appointment_date DESC,
            a.appointment_time DESC
        """,
        fetch=True
    ) or []

    if not appointments:

        st.info("No appointments found.")
        return

    df = pd.DataFrame(appointments)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

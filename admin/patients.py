import streamlit as st
import pandas as pd
from datetime import datetime, date, time, timedelta
from database import get_connection
from utils.functions import *

def admin_patients():

    st.title("👥 Manage Patients")

    patients = execute_query(
        """
        SELECT
            p.patient_id,
            u.name,
            u.email,
            u.phone,
            p.age,
            p.gender,
            p.address,
            p.emergency_contact
        FROM patients p
        JOIN users u ON p.user_id = u.id
        ORDER BY p.patient_id DESC
        """,
        fetch=True
    ) or []

    if not patients:

        st.info("No patients found.")
        return

    df = pd.DataFrame(patients)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

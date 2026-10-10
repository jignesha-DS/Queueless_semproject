import streamlit as st
import pandas as pd
from datetime import datetime, date, time, timedelta
from database import get_connection
from utils.functions import *

def patient_history():

    patient = get_patient()

    if not patient:
        return

    st.title("📜 Token History")

    history = get_patient_history(
        patient["patient_id"]
    )

    if not history:

        st.info("No token history available.")
        return

    df = pd.DataFrame(history)

    display_columns = [
        "token_number",
        "doctor_name",
        "specialization",
        "status",
        "visit_date"
    ]

    available_columns = [
        col for col in display_columns
        if col in df.columns
    ]

    st.dataframe(
        df[available_columns],
        use_container_width=True,
        hide_index=True
    )

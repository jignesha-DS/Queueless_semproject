import streamlit as st
import pandas as pd
from datetime import datetime, date, time, timedelta
from database import get_connection
from utils.functions import *

def admin_queue():

    st.title("📊 Queue Monitoring")

    queue = execute_query(
        """
        SELECT
            t.token_number,
            u.name AS patient_name,
            du.name AS doctor_name,
            d.specialization,
            t.status,
            t.queue_date,
            t.created_at
        FROM tokens t
        JOIN patients p
            ON t.patient_id = p.patient_id
        JOIN users u
            ON p.user_id = u.id
        JOIN doctors d
            ON t.doctor_id = d.doctor_id
        JOIN users du
            ON d.user_id = du.id
        WHERE t.queue_date = CURDATE()
        ORDER BY d.doctor_id, t.token_number
        """,
        fetch=True
    ) or []

    if not queue:

        st.info("No queue data for today.")
        return

    df = pd.DataFrame(queue)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    status_counts = (
        df["status"]
        .value_counts()
        .reset_index()
    )

    status_counts.columns = [
        "Status",
        "Count"
    ]

    st.subheader("Queue Status")

    st.bar_chart(
        status_counts.set_index("Status")
    )

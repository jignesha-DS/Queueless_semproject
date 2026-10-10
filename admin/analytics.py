import streamlit as st
import pandas as pd
from datetime import datetime, date, time, timedelta
from database import get_connection
from utils.functions import *

def admin_analytics():

    st.title("📈 Analytics & Reports")

    data = execute_query(
        """
        SELECT
            queue_date,
            COUNT(*) AS total_tokens,
            SUM(
                CASE
                    WHEN status = 'COMPLETED'
                    THEN 1 ELSE 0
                END
            ) AS completed,
            SUM(
                CASE
                    WHEN status = 'WAITING'
                    THEN 1 ELSE 0
                END
            ) AS waiting,
            SUM(
                CASE
                    WHEN status = 'CANCELLED'
                    THEN 1 ELSE 0
                END
            ) AS cancelled
        FROM tokens
        GROUP BY queue_date
        ORDER BY queue_date
        """,
        fetch=True
    ) or []

    if not data:

        st.info("No analytics data available.")
        return

    df = pd.DataFrame(data)

    df["queue_date"] = pd.to_datetime(
        df["queue_date"]
    )

    st.subheader("Daily Token Statistics")

    st.line_chart(
        df.set_index("queue_date")[
            [
                "total_tokens",
                "completed",
                "waiting",
                "cancelled"
            ]
        ]
    )

    st.subheader("Detailed Report")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

import streamlit as st
import pandas as pd
from datetime import datetime, date, time, timedelta
from database import get_connection
from utils.functions import *

def doctor_break():

    doctor = get_doctor()

    if not doctor:
        return

    st.title("⏸️ Doctor Break")

    start_date = st.date_input(
        "Break Date",
        value=date.today(),
        key="break_date"
    )

    start_time = st.time_input(
        "Break Start",
        value=time(13, 0),
        key="break_start"
    )

    end_time = st.time_input(
        "Break End",
        value=time(14, 0),
        key="break_end"
    )

    if st.button(
        "Schedule Break",
        key="schedule_break"
    ):

        if end_time <= start_time:

            st.error(
                "Break end time must be after start time."
            )
            return

        start_datetime = datetime.combine(
            start_date,
            start_time
        )

        end_datetime = datetime.combine(
            start_date,
            end_time
        )

        result = execute_query(
            """
            INSERT INTO doctor_breaks
            (
                doctor_id,
                break_start,
                break_end,
                status
            )
            VALUES (%s, %s, %s, 'ACTIVE')
            """,
            (
                doctor["doctor_id"],
                start_datetime,
                end_datetime
            )
        )

        if result:

            st.success(
                "Break scheduled successfully."
            )

    st.divider()

    breaks = execute_query(
        """
        SELECT *
        FROM doctor_breaks
        WHERE doctor_id = %s
        ORDER BY break_start DESC
        """,
        (doctor["doctor_id"],),
        fetch=True
    ) or []

    if breaks:

        df = pd.DataFrame(breaks)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

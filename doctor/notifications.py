import streamlit as st
import pandas as pd
from datetime import datetime, date, time, timedelta
from database import get_connection
from utils.functions import *

def doctor_notifications():

    st.title("🔔 Notifications")

    notifications = get_notifications(
        st.session_state.user_id
    )

    if not notifications:

        st.info("No notifications.")
        return

    for notification in notifications:

        if notification["is_read"]:

            st.info(
                notification["message"]
            )

        else:

            st.success(
                f"🔔 {notification['message']}"
            )

    if st.button(
        "Mark All as Read",
        key="doctor_mark_read"
    ):

        mark_notifications_read(
            st.session_state.user_id
        )

        st.rerun()

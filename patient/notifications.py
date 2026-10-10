import streamlit as st
import pandas as pd
from datetime import datetime, date, time, timedelta
from database import get_connection
from utils.functions import *

def patient_notifications():

    st.title("🔔 Notifications")

    notifications = get_notifications(
        st.session_state.user_id
    )

    if not notifications:

        st.info("No notifications yet.")
        return

    for notification in notifications:

        if notification["is_read"]:

            st.info(
                f"{notification['message']}\n\n"
                f"{notification['created_at']}"
            )

        else:

            st.success(
                f"🔔 {notification['message']}\n\n"
                f"{notification['created_at']}"
            )

    if st.button(
        "Mark All as Read",
        key="mark_notifications_read"
    ):

        mark_notifications_read(
            st.session_state.user_id
        )

        st.success("Notifications marked as read.")
        st.rerun()

import streamlit as st
import pandas as pd
from datetime import datetime, date, time, timedelta
from database import get_connection
from utils.functions import *

def admin_notifications():

    st.title("🔔 Send Notification")

    users = execute_query(
        """
        SELECT id, name, email, role
        FROM users
        ORDER BY name
        """,
        fetch=True
    ) or []

    if not users:
        st.info("No users available.")
        return

    user_options = {}

    for user in users:

        label = (
            f"{user['name']} "
            f"({user['role']}) - "
            f"{user['email']}"
        )

        user_options[label] = user

    selected = st.selectbox(
        "Select User",
        list(user_options.keys()),
        key="admin_notification_user"
    )

    user = user_options[selected]

    message = st.text_area(
        "Notification Message",
        key="admin_notification_message"
    )

    notification_type = st.selectbox(
        "Notification Type",
        [
            "GENERAL",
            "ANNOUNCEMENT",
            "QUEUE",
            "SYSTEM"
        ],
        key="admin_notification_type"
    )

    if st.button(
        "Send Notification",
        key="admin_send_notification"
    ):

        if not message:

            st.error("Please enter a message.")
            return

        create_notification(
            user["id"],
            message,
            notification_type
        )

        st.success(
            "Notification sent successfully."
        )

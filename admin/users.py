import streamlit as st
import pandas as pd
from datetime import datetime, date, time, timedelta
from database import get_connection
from utils.functions import *

def admin_users():

    st.title("👥 User Management")

    users = execute_query(
        """
        SELECT
            id,
            name,
            email,
            phone,
            role
        FROM users
        ORDER BY id DESC
        """,
        fetch=True
    ) or []

    if users:

        df = pd.DataFrame(users)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No users found.")

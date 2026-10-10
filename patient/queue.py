
import streamlit as st
from streamlit_autorefresh import st_autorefresh
from database import get_connection
from utils.functions import *


def patient_live_queue():

    patient = get_patient()

    if not patient:
        return

    st.title("🔴 Live Queue")

    # Manual refresh button
    col1, col2 = st.columns([3, 1])

    with col1:
        st.write("Track your token and waiting time.")

    with col2:
        if st.button("🔄 Refresh Queue"):
            st.rerun()

    # Automatically refresh every 5 seconds
    st_autorefresh(
        interval=5000,
        limit=None,
        key="patient_live_queue_refresh"
    )

    # Get the patient's token
    token = get_patient_token(
        patient["patient_id"]
    )

    if not token:
        st.info("You do not have an active token today.")
        return

    # Calculate people ahead and estimated waiting time
    people_ahead = get_people_ahead(
        token["doctor_id"],
        token["token_number"]
    )

    estimated_wait = (
        people_ahead * token["average_time"]
    )

    # Display token information
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
            <div class="token-box">
                <div>Your Token</div>
                <div class="token-number">
                    A-{token['token_number']:02d}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="stat-box">
                <h2>{people_ahead}</h2>
                <p>People Ahead</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class="stat-box">
                <h2>{estimated_wait} min</h2>
                <p>Estimated Wait</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    st.write(f"**Doctor:** Dr. {token['doctor_name']}")
    st.write(f"**Specialization:** {token['specialization']}")
    st.write(f"**Status:** `{token['status']}`")

    # Fetch today's active queue
    queue = execute_query(
        """
        SELECT
            t.token_number,
            t.status,
            u.name AS patient_name
        FROM tokens t
        JOIN patients p
            ON t.patient_id = p.patient_id
        JOIN users u
            ON p.user_id = u.id
        WHERE t.doctor_id = %s
          AND t.queue_date = CURDATE()
          AND UPPER(TRIM(t.status)) IN (
              'WAITING',
              'CALLED',
              'IN_PROGRESS'
          )
        ORDER BY t.token_number
        """,
        (token["doctor_id"],),
        fetch=True
    ) or []

    # Display active tokens only
    st.subheader("Today's Active Queue")

    if queue:
        for item in queue:

            token_text = (
                f"A-{item['token_number']:02d}"
            )

            if (
                item["token_number"]
                == token["token_number"]
            ):
                st.success(
                    f"🎫 {token_text} — YOU — "
                    f"{item['status']}"
                )
            else:
                st.write(
                    f"🎫 {token_text} — "
                    f"{item['patient_name']} — "
                    f"{item['status']}"
                )
    else:
        st.info("There are no active tokens in the queue.")

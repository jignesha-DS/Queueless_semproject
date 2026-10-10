import streamlit as st
import pandas as pd
from datetime import datetime, date, time, timedelta
from database import get_connection
from utils.functions import *

def doctor_queue():

    doctor = get_doctor()

    if not doctor:
        return

    st.title("🏥 Today's Queue")

    queue = get_doctor_queue(
        doctor["doctor_id"]
    )

    if not queue:

        st.info("No patients in today's queue.")
        return

    current = get_current_token(
        doctor["doctor_id"]
    )

    if current:

        st.success(
            f"Current Patient: "
            f"A-{current['token_number']:02d} - "
            f"{current['patient_name']} - "
            f"{current['status']}"
        )

    st.divider()

    for patient in queue:

        token_text = (
            f"A-{patient['token_number']:02d}"
        )

        status = patient["status"]

        with st.container(border=True):

            col1, col2, col3 = st.columns(
                [1, 3, 2]
            )

            with col1:
                st.subheader(token_text)

            with col2:

                st.write(
                    f"**Patient:** "
                    f"{patient['patient_name']}"
                )

                st.write(
                    f"Age: {patient.get('age', '-')}"
                )

                st.write(
                    f"Gender: {patient.get('gender', '-')}"
                )

            with col3:

                st.write(
                    f"**Status:** `{status}`"
                )

                if status == "WAITING":

                    if st.button(
                        "📢 Call Patient",
                        key=f"call_{patient['token_id']}"
                    ):

                        current_patient = get_current_token(
                            doctor["doctor_id"]
                        )

                        if current_patient:

                            st.warning(
                                "Please complete the current "
                                "patient before calling another."
                            )

                        else:

                            update = execute_query(
                                """
                                UPDATE tokens
                                SET
                                    status = 'CALLED',
                                    called_at = NOW()
                                WHERE token_id = %s
                                """,
                                (patient["token_id"],)
                            )

                            if update:

                                patient_user = execute_query(
                                    """
                                    SELECT user_id
                                    FROM patients
                                    WHERE patient_id = %s
                                    """,
                                    (patient["patient_id"],),
                                    fetch=True
                                )

                                if patient_user:

                                    create_notification(
                                        patient_user[0]["user_id"],
                                        f"Your token "
                                        f"A-{patient['token_number']:02d} "
                                        f"has been called. "
                                        f"Please proceed to the doctor.",
                                        "TOKEN_CALLED"
                                    )

                                st.success(
                                    f"Token {token_text} called."
                                )

                                st.rerun()

                elif status == "CALLED":

                    if st.button(
                        "▶️ Start Consultation",
                        key=f"start_{patient['token_id']}"
                    ):

                        update = execute_query(
                            """
                            UPDATE tokens
                            SET status = 'IN_PROGRESS'
                            WHERE token_id = %s
                            """,
                            (patient["token_id"],)
                        )

                        if update:

                            patient_user = execute_query(
                                """
                                SELECT user_id
                                FROM patients
                                WHERE patient_id = %s
                                """,
                                (patient["patient_id"],),
                                fetch=True
                            )

                            if patient_user:

                                create_notification(
                                    patient_user[0]["user_id"],
                                    f"Consultation for token "
                                    f"A-{patient['token_number']:02d} "
                                    f"has started.",
                                    "CONSULTATION_STARTED"
                                )

                            st.success(
                                "Consultation started."
                            )

                            st.rerun()

                elif status == "IN_PROGRESS":

                    if st.button(
                        "✅ Complete Consultation",
                        key=f"complete_{patient['token_id']}"
                    ):

                        update = execute_query(
                            """
                            UPDATE tokens
                            SET
                                status = 'COMPLETED',
                                completed_at = NOW()
                            WHERE token_id = %s
                            """,
                            (patient["token_id"],)
                        )

                        if update:

                            token_data = execute_query(
                                """
                                SELECT *
                                FROM tokens
                                WHERE token_id = %s
                                """,
                                (patient["token_id"],),
                                fetch=True
                            )

                            if token_data:

                                add_token_history(
                                    token_data[0]
                                )

                            patient_user = execute_query(
                                """
                                SELECT user_id
                                FROM patients
                                WHERE patient_id = %s
                                """,
                                (patient["patient_id"],),
                                fetch=True
                            )

                            if patient_user:

                                create_notification(
                                    patient_user[0]["user_id"],
                                    f"Your consultation for "
                                    f"token A-{patient['token_number']:02d} "
                                    f"has been completed.",
                                    "COMPLETED"
                                )

                            st.success(
                                "Consultation completed."
                            )

                            st.rerun()

                elif status == "COMPLETED":

                    st.success("Completed")

                elif status == "CANCELLED":

                    st.error("Cancelled")

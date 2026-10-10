
import streamlit as st
from datetime import datetime, date, time, timedelta
from database import get_connection


def execute_query(query, params=(), fetch=False, many=False):
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        if many:
            cursor.executemany(query, params)
        else:
            cursor.execute(query, params)

        if fetch:
            return cursor.fetchall()

        conn.commit()

        if cursor.lastrowid:
            return cursor.lastrowid

        return True

    except Exception as e:
        if conn:
            conn.rollback()
        st.error(f"Database error: {e}")
        return None

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def logout():
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.name = None
    st.session_state.role = None
    st.session_state.email = None
    st.rerun()


def get_patient():
    result = execute_query(
        """
        SELECT *
        FROM patients
        WHERE user_id = %s
        """,
        (st.session_state.user_id,),
        fetch=True
    )

    return result[0] if result else None


def get_doctor():
    result = execute_query(
        """
        SELECT d.*, u.name, u.email, u.phone
        FROM doctors d
        JOIN users u ON d.user_id = u.id
        WHERE d.user_id = %s
        """,
        (st.session_state.user_id,),
        fetch=True
    )

    return result[0] if result else None


def get_doctors():
    return execute_query(
        """
        SELECT
            d.doctor_id,
            d.specialization,
            d.degree,
            d.fees,
            d.address,
            d.experience,
            d.room_no,
            d.average_time,
            d.availability,
            u.name,
            u.email
        FROM doctors d
        JOIN users u ON d.user_id = u.id
        ORDER BY u.name
        """,
        fetch=True
    ) or []


def get_patient_token(patient_id):
    result = execute_query(
        """
        SELECT
            t.*,
            u.name AS doctor_name,
            d.specialization,
            d.average_time
        FROM tokens t
        JOIN doctors d
            ON t.doctor_id = d.doctor_id
        JOIN users u
            ON d.user_id = u.id
        WHERE t.patient_id = %s
          AND t.queue_date = CURDATE()
          AND UPPER(TRIM(t.status)) IN (
              'WAITING',
              'CALLED',
              'IN_PROGRESS'
          )
        ORDER BY t.token_id DESC
        LIMIT 1
        """,
        (patient_id,),
        fetch=True
    )

    return result[0] if result else None


def get_people_ahead(doctor_id, token_number):
    result = execute_query(
        """
        SELECT COUNT(*) AS count
        FROM tokens
        WHERE doctor_id = %s
          AND queue_date = CURDATE()
          AND token_number < %s
          AND UPPER(TRIM(status)) IN (
              'WAITING',
              'CALLED',
              'IN_PROGRESS'
          )
        """,
        (doctor_id, token_number),
        fetch=True
    )

    return result[0]["count"] if result else 0


def get_current_token(doctor_id):
    result = execute_query(
        """
        SELECT
            t.*,
            p.patient_id,
            u.name AS patient_name,
            p.age,
            p.gender
        FROM tokens t
        JOIN patients p ON t.patient_id = p.patient_id
        JOIN users u ON p.user_id = u.id
        WHERE t.doctor_id = %s
          AND t.queue_date = CURDATE()
          AND UPPER(TRIM(t.status)) IN (
              'CALLED',
              'IN_PROGRESS'
          )
        ORDER BY t.token_number
        LIMIT 1
        """,
        (doctor_id,),
        fetch=True
    )

    return result[0] if result else None


def get_next_token_number(doctor_id):
    result = execute_query(
        """
        SELECT COALESCE(MAX(token_number), 0) + 1 AS next_token
        FROM tokens
        WHERE doctor_id = %s
          AND queue_date = CURDATE()
        """,
        (doctor_id,),
        fetch=True
    )

    return result[0]["next_token"] if result else 1


def create_notification(
    user_id,
    message,
    notification_type="GENERAL"
):
    execute_query(
        """
        INSERT INTO notifications
        (user_id, message, notification_type)
        VALUES (%s, %s, %s)
        """,
        (user_id, message, notification_type)
    )


def get_notifications(user_id):
    return execute_query(
        """
        SELECT *
        FROM notifications
        WHERE user_id = %s
        ORDER BY created_at DESC
        LIMIT 20
        """,
        (user_id,),
        fetch=True
    ) or []


def mark_notifications_read(user_id):
    execute_query(
        """
        UPDATE notifications
        SET is_read = TRUE
        WHERE user_id = %s
        """,
        (user_id,)
    )


def add_token_history(token):
    existing = execute_query(
        """
        SELECT history_id
        FROM token_history
        WHERE token_id = %s
          AND status = %s
        """,
        (token["token_id"], token["status"]),
        fetch=True
    )

    if existing:
        return

    execute_query(
        """
        INSERT INTO token_history
        (
            token_id,
            patient_id,
            doctor_id,
            token_number,
            status,
            visit_date
        )
        VALUES (%s, %s, %s, %s, %s, CURDATE())
        """,
        (
            token["token_id"],
            token["patient_id"],
            token["doctor_id"],
            token["token_number"],
            token["status"]
        )
    )


def get_patient_history(patient_id):
    return execute_query(
        """
        SELECT
            h.*,
            u.name AS doctor_name,
            d.specialization
        FROM token_history h
        JOIN doctors d ON h.doctor_id = d.doctor_id
        JOIN users u ON d.user_id = u.id
        WHERE h.patient_id = %s
        ORDER BY h.visit_date DESC, h.created_at DESC
        """,
        (patient_id,),
        fetch=True
    ) or []


def get_doctor_queue(doctor_id):
    return execute_query(
        """
        SELECT
            t.*,
            u.name AS patient_name,
            p.age,
            p.gender,
            p.address,
            p.emergency_contact
        FROM tokens t
        JOIN patients p ON t.patient_id = p.patient_id
        JOIN users u ON p.user_id = u.id
        WHERE t.doctor_id = %s
          AND t.queue_date = CURDATE()
        ORDER BY t.token_number
        """,
        (doctor_id,),
        fetch=True
    ) or []



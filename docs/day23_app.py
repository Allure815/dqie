# =========================================
# DAY 23 - ALERT LIFECYCLE + RECOVERY SYSTEM
# =========================================

import streamlit as st
import psycopg2
import pandas as pd
import time


# -----------------------------------------
# STEP 1: DB CONNECTION
# -----------------------------------------
def get_connection():
    return psycopg2.connect(
        dbname="db_pulse_lab",
        user="postgres",
        password="postgres123",
        host="localhost",
        port="5432"
    )


# -----------------------------------------
# STEP 2: FETCH INCIDENTS
# -----------------------------------------
def fetch_incidents():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM incidents;", conn)
    conn.close()
    return df


# -----------------------------------------
# STEP 3: GENERATE CURRENT STATE
# -----------------------------------------
def generate_state(df):

    high_risk = len(df[df["risk_score"] >= 80])
    blocked = len(df[df["issue_type"] == "BLOCKED"])

    if blocked > 0:
        return "CRITICAL", "Blocking detected", "error"

    elif high_risk > 5:
        return "WARNING", "High risk queries increasing", "warning"

    else:
        return "HEALTHY", "System is stable", "success"


# -----------------------------------------
# STEP 4: GET LAST ALERT
# -----------------------------------------
def get_last_alert():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT message, alert_type
        FROM alerts
        ORDER BY created_time DESC
        LIMIT 1;
    """)

    result = cursor.fetchone()
    conn.close()
    return result


# -----------------------------------------
# STEP 5: SAVE ALERT
# -----------------------------------------
def save_alert(message, alert_type):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO alerts (message, alert_type)
        VALUES (%s, %s);
    """, (message, alert_type))

    conn.commit()
    conn.close()


# -----------------------------------------
# STEP 6: FETCH ALERT HISTORY
# -----------------------------------------
def fetch_alerts():
    conn = get_connection()
    df = pd.read_sql("""
        SELECT alert_id, message, alert_type, created_time
        FROM alerts
        ORDER BY created_time DESC
        LIMIT 10;
    """, conn)
    conn.close()
    return df


# =========================================
# UI START
# =========================================

st.title("🧠 DB Monitoring - Lifecycle Aware System")

refresh_interval = st.slider("Refresh Interval", 2, 10, 5)


while True:

    # STEP A: GET DATA
    df = fetch_incidents()

    # STEP B: GET CURRENT STATE
    state, message, level = generate_state(df)

    # STEP C: DISPLAY CURRENT STATUS
    st.subheader("🚨 Live Status")

    if level == "error":
        st.error(message)
    elif level == "warning":
        st.warning(message)
    else:
        st.success(message)

    # STEP D: GET LAST ALERT
    last_alert = get_last_alert()

    # -----------------------------------------
    # STEP E: LIFECYCLE LOGIC (VERY IMPORTANT)
    # -----------------------------------------

    if last_alert is None:
        # First alert ever
        if state != "HEALTHY":
            save_alert(f"ALERT: {message}", level)

    else:
        last_message, last_type = last_alert

        # CASE 1: PROBLEM STARTED
        if state != "HEALTHY" and "ALERT" not in last_message:
            save_alert(f"ALERT: {message}", level)

        # CASE 2: PROBLEM RESOLVED (RECOVERY)
        elif state == "HEALTHY" and "ALERT" in last_message:
            save_alert("RECOVERY: System back to normal", "success")


    # -----------------------------------------
    # STEP F: SHOW HISTORY
    # -----------------------------------------
    st.subheader("📜 Alert History")

    alert_df = fetch_alerts()
    st.dataframe(alert_df)


    # STEP G: WAIT + REFRESH
    time.sleep(refresh_interval)
    st.rerun()

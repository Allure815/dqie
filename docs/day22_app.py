# =========================================
# DAY 22 - SMART ALERT SYSTEM (NO DUPLICATES)
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
    query = "SELECT * FROM incidents;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df


# -----------------------------------------
# STEP 3: GENERATE ALERT
# -----------------------------------------
def generate_alert(df):

    high_risk = len(df[df["risk_score"] >= 80])
    blocked = len(df[df["issue_type"] == "BLOCKED"])

    if blocked > 0:
        return "CRITICAL: Blocking detected!", "error"

    elif high_risk > 5:
        return "WARNING: High risk queries increasing!", "warning"

    else:
        return "System is stable", "success"


# -----------------------------------------
# STEP 4: GET LAST ALERT (VERY IMPORTANT)
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

    return result   # returns (message, type) OR None


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
    query = """
        SELECT alert_id, message, alert_type, created_time
        FROM alerts
        ORDER BY created_time DESC
        LIMIT 10;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df


# =========================================
# UI STARTS HERE
# =========================================

st.title("🧠 Smart DB Monitoring System (No Duplicate Alerts)")

refresh_interval = st.slider("Refresh Interval (seconds)", 2, 10, 5)


while True:

    # -----------------------------------------
    # LOAD INCIDENT DATA
    # -----------------------------------------
    df = fetch_incidents()


    # -----------------------------------------
    # GENERATE ALERT
    # -----------------------------------------
    message, level = generate_alert(df)


    # -----------------------------------------
    # DISPLAY ALERT
    # -----------------------------------------
    st.subheader("🚨 Live Status")

    if level == "error":
        st.error(message)
    elif level == "warning":
        st.warning(message)
    else:
        st.success(message)


    # -----------------------------------------
    # SMART SAVE (DAY 22 CORE LOGIC)
    # -----------------------------------------
    last_alert = get_last_alert()

    if level != "success":

        # First alert ever
        if last_alert is None:
            save_alert(message, level)

        else:
            last_message, last_type = last_alert

            # Save only if different
            if message != last_message or level != last_type:
                save_alert(message, level)


    # -----------------------------------------
    # SHOW ALERT HISTORY
    # -----------------------------------------
    st.subheader("📜 Alert History (Last 10)")

    alert_df = fetch_alerts()
    st.dataframe(alert_df)


    # -----------------------------------------
    # WAIT + REFRESH
    # -----------------------------------------
    time.sleep(refresh_interval)
    st.rerun()

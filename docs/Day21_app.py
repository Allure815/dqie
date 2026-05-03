# =========================================
# DAY 21 - ALERT LOGGING + HISTORY
# =========================================

import streamlit as st
import psycopg2
import pandas as pd
import time


# -----------------------------------------
# DB CONNECTION
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
# FETCH INCIDENTS
# -----------------------------------------
def fetch_incidents():
    conn = get_connection()
    query = "SELECT * FROM incidents;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df


# -----------------------------------------
# GENERATE ALERT
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
# SAVE ALERT TO DB
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
# FETCH ALERT HISTORY
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
# UI STARTS
# =========================================

st.title("🧠 DB Monitoring + Alert History")

refresh_interval = st.slider("Refresh Interval", 2, 10, 5)


while True:

    # -----------------------------------------
    # LOAD DATA
    # -----------------------------------------
    df = fetch_incidents()

    # -----------------------------------------
    # GENERATE ALERT
    # -----------------------------------------
    message, level = generate_alert(df)

    st.subheader("🚨 Live Status")

    if level == "error":
        st.error(message)
    elif level == "warning":
        st.warning(message)
    else:
        st.success(message)

    # -----------------------------------------
    # SAVE ALERT (IMPORTANT)
    # -----------------------------------------
    if level != "success":   # avoid saving normal state
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

# =========================================
# DAY 25 - INTELLIGENT DB MONITORING SYSTEM
# (Lifecycle + Duration + Analytics + Anomaly)
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
        dbname="ab_pulse_lab",
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
    df = pd.read_sql("SELECT * FROM incidents;", conn)
    conn.close()
    return df


# -----------------------------------------
# GENERATE STATE
# -----------------------------------------
def generate_state(df):

    high_risk = len(df[df["risk_score"] >= 80])
    blocked = len(df[df["issue_type"] == "BLOCKED"])

    if blocked > 0:
        return "CRITICAL", "Blocking detected", "error"

    elif high_risk > 5:
        return "WARNING", "High risk queries", "warning"

    else:
        return "HEALTHY", "System stable", "success"


# -----------------------------------------
# GET LAST ALERT
# -----------------------------------------
def get_last_alert():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT alert_id, message, alert_type, end_time
        FROM alerts
        ORDER BY created_time DESC
        LIMIT 1;
    """)

    result = cursor.fetchone()
    conn.close()
    return result


# -----------------------------------------
# SAVE ALERT
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
# CLOSE ALERT (SET END TIME)
# -----------------------------------------
def close_alert(alert_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE alerts
        SET end_time = NOW()
        WHERE alert_id = %s;
    """, (alert_id,))

    conn.commit()
    conn.close()


# -----------------------------------------
# FETCH COMPLETED ALERTS (WITH DURATION)
# -----------------------------------------
def fetch_alerts():
    conn = get_connection()

    query = """
        SELECT 
            alert_id,
            message,
            alert_type,
            created_time,
            end_time,
            EXTRACT(EPOCH FROM (end_time - created_time)) AS duration_seconds
        FROM alerts
        WHERE end_time IS NOT NULL
        ORDER BY created_time DESC;
    """

    df = pd.read_sql(query, conn)
    conn.close()
    return df


# -----------------------------------------
# ANOMALY DETECTION
# -----------------------------------------
def detect_anomaly(df):

    if df.empty:
        return None

    avg_duration = df["duration_seconds"].mean()
    latest_duration = df["duration_seconds"].iloc[-1]

    if latest_duration > 2 * avg_duration:
        return f"⚠️ ANOMALY: Duration spike ({round(latest_duration,2)} sec)"

    return None


# =========================================
# UI START
# =========================================

st.title("🧠 Intelligent DB Monitoring System (Day 25)")

refresh_interval = st.slider("Refresh Interval", 2, 10, 5)


while True:

    # -----------------------------------------
    # STEP 1: FETCH INCIDENTS
    # -----------------------------------------
    df = fetch_incidents()

    # -----------------------------------------
    # STEP 2: DETERMINE STATE
    # -----------------------------------------
    state, message, level = generate_state(df)

    # -----------------------------------------
    # STEP 3: SHOW STATUS
    # -----------------------------------------
    st.subheader("🚨 Live Status")

    if level == "error":
        st.error(message)
    elif level == "warning":
        st.warning(message)
    else:
        st.success(message)

    # -----------------------------------------
    # STEP 4: LIFECYCLE HANDLING
    # -----------------------------------------
    last = get_last_alert()

    if last is None:
        if state != "HEALTHY":
            save_alert(f"ALERT: {message}", level)

    else:
        alert_id, last_msg, last_type, end_time = last

        # START NEW ALERT
        if state != "HEALTHY" and end_time is not None:
            save_alert(f"ALERT: {message}", level)

        # CLOSE ALERT
        elif state == "HEALTHY" and end_time is None:
            close_alert(alert_id)

    # -----------------------------------------
    # STEP 5: ANALYTICS
    # -----------------------------------------
    st.subheader("📊 Analytics")

    alerts_df = fetch_alerts()

    if not alerts_df.empty:

        total_alerts = len(alerts_df)
        avg_duration = alerts_df["duration_seconds"].mean()
        max_duration = alerts_df["duration_seconds"].max()

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Alerts", total_alerts)
        col2.metric("Avg Duration (sec)", round(avg_duration, 2))
        col3.metric("Max Duration (sec)", round(max_duration, 2))

        st.bar_chart(alerts_df["duration_seconds"])

    else:
        st.info("No completed alerts yet")

    # -----------------------------------------
    # STEP 6: ANOMALY DETECTION
    # -----------------------------------------
    anomaly_msg = detect_anomaly(alerts_df)

    if anomaly_msg:
        st.warning(anomaly_msg)

    # -----------------------------------------
    # STEP 7: SHOW DATA
    # -----------------------------------------
    st.subheader("📜 Completed Alerts")
    st.dataframe(alerts_df)

    # -----------------------------------------
    # REFRESH
    # -----------------------------------------
    time.sleep(refresh_interval)
    st.rerun()

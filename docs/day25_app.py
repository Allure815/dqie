import streamlit as st
import psycopg2
import pandas as pd
import time


# DB CONNECTION
def get_connection():
    return psycopg2.connect(
        dbname="dqie_lab",
        user="postgres",
        password="postgres123",
        host="localhost",
        port="5432"
    )


# FETCH INCIDENTS
def fetch_incidents():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM incidents;", conn)
    conn.close()
    return df


# STATE LOGIC
def generate_state(df):
    high_risk = len(df[df["risk_score"] >= 80])
    blocked = len(df[df["issue_type"] == "BLOCKED"])

    if blocked > 0:
        return "CRITICAL", "Blocking detected", "error"
    elif high_risk > 1:
        return "WARNING", "High risk queries", "warning"
    else:
        return "HEALTHY", "System stable", "success"


# GET LAST ALERT
def get_last_alert():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT alert_id, message, alert_type, end_time
        FROM alerts
        ORDER BY created_time DESC
        LIMIT 1;
    """)
    res = cur.fetchone()
    conn.close()
    return res


# SAVE ALERT
def save_alert(msg, level):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO alerts (message, alert_type) VALUES (%s, %s)",
        (msg, level)
    )
    conn.commit()
    conn.close()


# CLOSE ALERT
def close_alert(alert_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE alerts SET end_time = NOW() WHERE alert_id = %s",
        (alert_id,)
    )
    conn.commit()
    conn.close()


# FETCH ALERTS WITH DURATION
def fetch_alerts():
    conn = get_connection()
    df = pd.read_sql("""
        SELECT *,
        EXTRACT(EPOCH FROM (end_time - created_time)) AS duration_seconds
        FROM alerts
        WHERE end_time IS NOT NULL;
    """, conn)
    conn.close()
    return df


# ANOMALY DETECTION
def detect_anomaly(df):
    if df.empty:
        return None

    avg = df["duration_seconds"].mean()
    latest = df["duration_seconds"].iloc[-1]

    if latest > 2 * avg:
        return f"⚠️ Anomaly: {round(latest,2)} sec spike"

    return None


# UI
st.title("🧠 DQIE - Intelligent Monitoring")

while True:

    df = fetch_incidents()
    state, msg, level = generate_state(df)

    st.subheader("Live Status")

    if level == "error":
        st.error(msg)
    elif level == "warning":
        st.warning(msg)
    else:
        st.success(msg)

    last = get_last_alert()

    if last is None:
        if state != "HEALTHY":
            save_alert("ALERT: " + msg, level)
    else:
        alert_id, last_msg, last_type, end_time = last

        if state != "HEALTHY" and end_time is not None:
            save_alert("ALERT: " + msg, level)

        elif state == "HEALTHY" and end_time is None:
            close_alert(alert_id)

    alerts_df = fetch_alerts()

    st.subheader("Analytics")

    if not alerts_df.empty:
        st.metric("Total Alerts", len(alerts_df))
        st.metric("Avg Duration", round(alerts_df["duration_seconds"].mean(), 2))
        st.bar_chart(alerts_df["duration_seconds"])

    anomaly = detect_anomaly(alerts_df)

    if anomaly:
        st.warning(anomaly)

    st.dataframe(alerts_df)

    time.sleep(5)
    st.rerun()

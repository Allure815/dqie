# =========================================
# DAY 26 - INTELLIGENT + PREDICTIVE SYSTEM
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
        dbname="dqie_lab",
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
# STATE LOGIC
# -----------------------------------------
def generate_state(df):
    high_risk = len(df[df["risk_score"] >= 80])
    blocked = len(df[df["issue_type"] == "BLOCKED"])

    if blocked > 0:
        return "CRITICAL", "Blocking detected", "error"
    elif high_risk > 1:
        return "WARNING", "High risk queries", "warning"
    else:
        return "HEALTHY", "System stable", "success"


# -----------------------------------------
# ALERT FUNCTIONS
# -----------------------------------------
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


def save_alert(msg, level):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO alerts (message, alert_type) VALUES (%s, %s)",
        (msg, level)
    )
    conn.commit()
    conn.close()


def close_alert(alert_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE alerts SET end_time = NOW() WHERE alert_id = %s",
        (alert_id,)
    )
    conn.commit()
    conn.close()


# -----------------------------------------
# FETCH ALERTS WITH DURATION
# -----------------------------------------
def fetch_alerts():
    conn = get_connection()
    df = pd.read_sql("""
        SELECT *,
        EXTRACT(EPOCH FROM (end_time - created_time)) AS duration_seconds
        FROM alerts
        WHERE end_time IS NOT NULL
        ORDER BY created_time;
    """, conn)
    conn.close()
    return df


# -----------------------------------------
# ANOMALY DETECTION
# -----------------------------------------
def detect_anomaly(df):

    if df.empty:
        return None

    avg = df["duration_seconds"].mean()
    latest = df["duration_seconds"].iloc[-1]

    if latest > 2 * avg:
        return f"⚠️ Anomaly: Spike detected ({round(latest,2)} sec)"

    return None


# -----------------------------------------
# TREND DETECTION
# -----------------------------------------
def detect_trend(df):

    if len(df) < 3:
        return None

    last3 = df["duration_seconds"].tail(3).values

    if last3[0] < last3[1] < last3[2]:
        return "📈 Increasing trend (system degrading)"

    elif last3[0] > last3[1] > last3[2]:
        return "📉 Decreasing trend (system improving)"

    else:
        return "➖ No clear trend"


# -----------------------------------------
# PREDICTION
# -----------------------------------------
def predict_next(df):

    if len(df) < 2:
        return None

    last2 = df["duration_seconds"].tail(2).values
    increase = last2[1] - last2[0]
    prediction = last2[1] + increase

    return round(prediction, 2)


# =========================================
# UI START
# =========================================

st.title("🧠 DQIE - Intelligent + Predictive Monitoring")

refresh_interval = st.slider("Refresh Interval", 2, 10, 5)


while True:

    # -----------------------------------------
    # STEP 1: FETCH INCIDENTS
    # -----------------------------------------
    df = fetch_incidents()

    # -----------------------------------------
    # STEP 2: CURRENT STATE
    # -----------------------------------------
    state, msg, level = generate_state(df)

    st.subheader("🚨 Live Status")

    if level == "error":
        st.error(msg)
    elif level == "warning":
        st.warning(msg)
    else:
        st.success(msg)

    # -----------------------------------------
    # STEP 3: ALERT LIFECYCLE
    # -----------------------------------------
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

    # -----------------------------------------
    # STEP 4: ANALYTICS
    # -----------------------------------------
    alerts_df = fetch_alerts()

    st.subheader("📊 Analytics")

    if not alerts_df.empty:

        total = len(alerts_df)
        avg = alerts_df["duration_seconds"].mean()
        max_val = alerts_df["duration_seconds"].max()

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Alerts", total)
        col2.metric("Avg Duration", round(avg, 2))
        col3.metric("Max Duration", round(max_val, 2))

        st.bar_chart(alerts_df["duration_seconds"])

    else:
        st.info("No completed alerts yet")

    # -----------------------------------------
    # STEP 5: ANOMALY
    # -----------------------------------------
    anomaly = detect_anomaly(alerts_df)

    if anomaly:
        st.warning(anomaly)

    # -----------------------------------------
    # STEP 6: TREND
    # -----------------------------------------
    trend = detect_trend(alerts_df)

    st.subheader("📈 Trend & Prediction")

    if trend:
        st.info(trend)

    # -----------------------------------------
    # STEP 7: PREDICTION
    # -----------------------------------------
    prediction = predict_next(alerts_df)

    if prediction:
        st.info(f"🔮 Next predicted duration: {prediction} sec")

    # -----------------------------------------
    # STEP 8: DATA VIEW
    # -----------------------------------------
    st.subheader("📜 Completed Alerts")
    st.dataframe(alerts_df)

    # -----------------------------------------
    # REFRESH
    # -----------------------------------------
    time.sleep(refresh_interval)
    st.rerun()

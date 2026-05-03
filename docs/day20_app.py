# =========================================
# DAY 20 - REAL TIME MONITORING + ALERTS
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
    query = """
        SELECT 
            incident_id,
            pid,
            LEFT(query, 50) || '...' AS query,
            duration,
            issue_type,
            root_cause,
            risk_score,
            recommendation,
            created_time
        FROM incidents;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df


# -----------------------------------------
# STEP 3: ALERT LOGIC
# -----------------------------------------
def generate_alert(df):

    high_risk_count = len(df[df["risk_score"] >= 80])
    blocked_count = len(df[df["issue_type"] == "BLOCKED"])

    # Critical condition
    if blocked_count > 0:
        return "CRITICAL: Blocking detected!", "error"

    # Warning condition
    elif high_risk_count > 5:
        return "WARNING: Many high-risk queries!", "warning"

    # Healthy
    else:
        return "System is stable", "success"


# =========================================
# UI STARTS
# =========================================

st.title("⚡ Real-Time DB Monitoring Dashboard")

# Auto refresh control
refresh_interval = st.slider("Refresh Interval (seconds)", 2, 10, 5)


# Infinite loop for real-time simulation
while True:

    # -----------------------------------------
    # LOAD DATA
    # -----------------------------------------
    df = fetch_incidents()

    # -----------------------------------------
    # ALERT SYSTEM
    # -----------------------------------------
    message, level = generate_alert(df)

    st.subheader("🚨 System Status")

    if level == "error":
        st.error(message)
    elif level == "warning":
        st.warning(message)
    else:
        st.success(message)


    # -----------------------------------------
    # METRICS
    # -----------------------------------------
    st.subheader("📈 Metrics")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total", len(df))

    with col2:
        st.metric("High Risk", len(df[df["risk_score"] >= 80]))

    with col3:
        st.metric("Blocked", len(df[df["issue_type"] == "BLOCKED"]))


    # -----------------------------------------
    # CHART
    # -----------------------------------------
    st.subheader("📊 Issue Distribution")

    chart_data = df["issue_type"].value_counts()
    st.bar_chart(chart_data)


    # -----------------------------------------
    # TABLE
    # -----------------------------------------
    st.subheader("📌 Live Incidents")

    st.dataframe(df)


    # Wait before refresh
    time.sleep(refresh_interval)

    # Rerun app
    st.rerun()

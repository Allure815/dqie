# =========================================
# DAY 28 - SAFE AUTOMATION SYSTEM
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
# RISK DETECTION
# -----------------------------------------
def get_critical_pid():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT pid
        FROM incidents
        WHERE risk_score >= 80
        LIMIT 1;
    """)

    result = cur.fetchone()
    conn.close()

    return result[0] if result else None


# -----------------------------------------
# LOG ACTION
# -----------------------------------------
def log_action(action_type, pid, status):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO action_logs (action_type, target_pid, status)
        VALUES (%s, %s, %s)
    """, (action_type, pid, status))

    conn.commit()
    conn.close()


# -----------------------------------------
# SAFE QUERY TERMINATION
# -----------------------------------------
def kill_query(pid):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(f"SELECT pg_terminate_backend({pid});")

        conn.commit()
        conn.close()

        log_action("KILL_QUERY", pid, "SUCCESS")

        return "✅ Query terminated successfully"

    except Exception as e:
        log_action("KILL_QUERY", pid, "FAILED")
        return f"❌ Failed: {str(e)}"


# -----------------------------------------
# FETCH LOGS
# -----------------------------------------
def fetch_logs():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM action_logs ORDER BY created_time DESC;", conn)
    conn.close()
    return df


# =========================================
# UI START
# =========================================

st.title("🧠 DQIE - Safe Automation Engine (Day 28)")

refresh_interval = st.slider("Refresh Interval", 2, 10, 5)


while True:

    # -----------------------------------------
    # INCIDENT VIEW
    # -----------------------------------------
    st.subheader("📊 Incidents")
    incidents_df = fetch_incidents()
    st.dataframe(incidents_df)

    # -----------------------------------------
    # AUTOMATION PANEL
    # -----------------------------------------
    st.subheader("⚙️ Automation Control Panel")

    pid = get_critical_pid()

    if pid:
        st.warning(f"High-risk query detected (PID: {pid})")

        if st.button("Terminate Query (Manual Approval Required)"):
            result = kill_query(pid)
            st.success(result)

    else:
        st.success("No critical query found")

    # -----------------------------------------
    # ACTION LOGS
    # -----------------------------------------
    st.subheader("📜 Action Logs")

    logs_df = fetch_logs()
    st.dataframe(logs_df)

    # -----------------------------------------
    # REFRESH
    # -----------------------------------------
    time.sleep(refresh_interval)
    st.rerun()

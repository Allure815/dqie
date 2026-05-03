# DAY 19 - DASHBOARD (CHARTS + FILTERS)
# =========================================

import streamlit as st
import psycopg2
import pandas as pd   # 👉 used for charts + table handling


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
    df = pd.read_sql(query, conn)   # 👉 directly into dataframe
    conn.close()
    return df


# -----------------------------------------
# STEP 3: FETCH ANALYSIS
# -----------------------------------------
def fetch_analysis():
    conn = get_connection()
    query = """
        SELECT issue_type, COUNT(*) as count
        FROM incidents
        GROUP BY issue_type
        ORDER BY count DESC;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df


# -----------------------------------------
# STEP 4: FETCH SUMMARY
# -----------------------------------------
def fetch_summary():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
        CASE
            WHEN COUNT(*) FILTER (WHERE issue_type = 'BLOCKED') >
                 COUNT(*) FILTER (WHERE issue_type = 'SLOW')
            THEN 'Most issues are BLOCKED queries'

            WHEN COUNT(*) FILTER (WHERE issue_type = 'SLOW') >
                 COUNT(*) FILTER (WHERE issue_type = 'BLOCKED')
            THEN 'Most issues are SLOW queries'

            ELSE 'System is balanced'
        END
        FROM incidents;
    """)

    result = cursor.fetchone()
    conn.close()
    return result[0]


# =========================================
# UI STARTS HERE
# =========================================

st.title("📊 DB Query Intelligence Engine Dashboard")


# -----------------------------------------
# STEP 5: LOAD DATA
# -----------------------------------------
incidents_df = fetch_incidents()
analysis_df = fetch_analysis()
summary = fetch_summary()


# -----------------------------------------
# STEP 6: METRICS
# -----------------------------------------
st.subheader("📈 Key Metrics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Incidents", len(incidents_df))

with col2:
    st.metric("High Risk", len(incidents_df[incidents_df["risk_score"] >= 80]))

with col3:
    st.metric("Slow Queries", len(incidents_df[incidents_df["issue_type"] == "SLOW"]))


# -----------------------------------------
# STEP 7: CHART
# -----------------------------------------
st.subheader("📊 Issue Type Distribution")

st.bar_chart(analysis_df.set_index("issue_type"))


# -----------------------------------------
# STEP 8: FILTER
# -----------------------------------------
st.subheader("🎛 Filter Data")

selected_issue = st.selectbox(
    "Select Issue Type",
    ["ALL"] + list(analysis_df["issue_type"])
)

if selected_issue != "ALL":
    filtered_df = incidents_df[incidents_df["issue_type"] == selected_issue]
else:
    filtered_df = incidents_df


# -----------------------------------------
# STEP 9: TABLE DISPLAY
# -----------------------------------------
st.subheader("📌 Incidents Table")

st.dataframe(filtered_df)


# -----------------------------------------
# STEP 10: SUMMARY
# -----------------------------------------
st.subheader("🧠 System Insight")

st.success(summary)

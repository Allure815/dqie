# ================================
# DAY 18 - STREAMLIT UI APP
# ================================

# Step 1: Import libraries
import streamlit as st
import psycopg2


# Step 2: Connect to database
def get_connection():
    return psycopg2.connect(
        dbname="db_pulse_lab",   # 👉 change
        user="postgres",
        password="postgres123",     # 👉 change
        host="localhost",
        port="5432"
    )


# Step 3: Fetch all incidents
def fetch_incidents():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM incidents;")
    data = cursor.fetchall()

    conn.close()
    return data


# Step 4: Fetch issue analysis
def fetch_analysis():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT issue_type, COUNT(*) 
        FROM incidents
        GROUP BY issue_type
        ORDER BY COUNT(*) DESC;
    """)

    data = cursor.fetchall()
    conn.close()
    return data


# Step 5: Fetch summary
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

            ELSE 'System has balanced or minimal issues'
        END
        FROM incidents;
    """)

    result = cursor.fetchone()
    conn.close()
    return result[0]


# ================================
# UI STARTS HERE
# ================================

# Step 6: Title
st.title("📊 DQIE DB Query Intelligence Engine")


# Step 7: Show incidents table
st.subheader("📌 All Incidents")

incidents = fetch_incidents()

# Convert to readable format
columns = ["ID", "PID", "Query", "Duration", "Issue", "Root Cause", "Risk", "Recommendation", "Time"]
st.dataframe([dict(zip(columns, row)) for row in incidents])


# Step 8: Show analysis
st.subheader("📊 Issue Analysis")

analysis = fetch_analysis()

for row in analysis:
    st.write(f"Issue Type: {row[0]} | Count: {row[1]}")


# Step 9: Show summary
st.subheader("🧠 System Summary")

summary = fetch_summary()

st.success(summary)

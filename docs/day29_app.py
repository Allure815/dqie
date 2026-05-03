# ============================================================
# 🧠 DQIE - DAY 29 (CLEAN ARCHITECTURE SYSTEM)
# ============================================================
# This application demonstrates a production-style structure:
# ✔ Data Layer (DB connection)
# ✔ Data Fetch Layer
# ✔ Processing Layer
# ✔ Automation Layer
# ✔ UI Layer
# ============================================================


# ============================================================
# 📦 IMPORT LIBRARIES
# ============================================================

import streamlit as st          # UI framework
import psycopg2                # PostgreSQL connection
import pandas as pd            # Data handling


# ============================================================
# 🧱 DATA LAYER (DATABASE CONNECTION)
# ============================================================
# This function connects Python to PostgreSQL database

def get_connection():
    return psycopg2.connect(
        dbname="dqie_lab",      # Your database name
        user="postgres",        # DB username
        password="postgres123",  # Replace with your password
        host="localhost",       # DB host
        port="5432"             # Default PostgreSQL port
    )


# ============================================================
# 📥 DATA FETCH LAYER (READ DATA FROM DATABASE)
# ============================================================

# 🔹 Fetch all incidents (latest first)
def fetch_incidents():
    conn = get_connection()  # Open DB connection
    
    # Read data into pandas DataFrame
    df = pd.read_sql(
        "SELECT * FROM incidents ORDER BY created_time DESC;",
        conn
    )
    
    conn.close()  # Close connection
    return df


# 🔹 Fetch all action logs (latest first)
def fetch_logs():
    conn = get_connection()
    
    df = pd.read_sql(
        "SELECT * FROM action_logs ORDER BY created_time DESC;",
        conn
    )
    
    conn.close()
    return df


# ============================================================
# ⚙️ PROCESSING LAYER (BUSINESS LOGIC)
# ============================================================

# 🔹 Identify critical query (high risk)
def get_critical_pid():
    conn = get_connection()
    cur = conn.cursor()
    
    # Select most recent high-risk query
    cur.execute("""
        SELECT pid
        FROM incidents
        WHERE risk_score >= 80
        ORDER BY created_time DESC
        LIMIT 1;
    """)
    
    result = cur.fetchone()  # Get one row
    conn.close()
    
    # Return PID if found, else None
    return result[0] if result else None


# ============================================================
# 🤖 AUTOMATION LAYER (ACTION EXECUTION)
# ============================================================

# 🔹 Log any action taken by system
def log_action(action_type, pid, status):
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        # Insert log record
        cur.execute("""
            INSERT INTO action_logs (action_type, target_pid, status)
            VALUES (%s, %s, %s)
        """, (action_type, pid, status))
        
        conn.commit()   # Save changes
        conn.close()
        
    except Exception as e:
        print("Logging failed:", e)


# 🔹 Safely terminate query (requires permission)
def kill_query(pid):
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        # PostgreSQL function to terminate backend process
        cur.execute(f"SELECT pg_terminate_backend({pid});")
        
        conn.commit()
        conn.close()
        
        # Log success
        log_action("KILL_QUERY", pid, "SUCCESS")
        
        return "✅ Query terminated successfully"
    
    except Exception as e:
        # Log failure
        log_action("KILL_QUERY", pid, "FAILED")
        
        return f"❌ Failed: {str(e)}"


# ============================================================
# 🖥️ UI LAYER (STREAMLIT APPLICATION)
# ============================================================

# 🔹 App Title
st.title("🧠 DQIE - Day 29 Clean Architecture System")


# ============================================================
# 📊 INCIDENT DISPLAY SECTION
# ============================================================

st.subheader("📊 Incidents (Live Data)")

# Fetch and display incidents
incidents_df = fetch_incidents()
st.dataframe(incidents_df)


# ============================================================
# ⚙️ AUTOMATION CONTROL PANEL
# ============================================================

st.subheader("⚙️ Automation Panel")

# Get critical query PID
pid = get_critical_pid()

if pid:
    # Show warning if critical query exists
    st.warning(f"🚨 Critical query detected (PID: {pid})")
    
    # Manual approval button
    if st.button("Terminate Query (Manual Approval Required)"):
        result = kill_query(pid)
        st.success(result)

else:
    # If no critical query
    st.success("✅ System Stable - No Critical Issues")


# ============================================================
# 📜 ACTION LOGS DISPLAY
# ============================================================

st.subheader("📜 Action Logs")

logs_df = fetch_logs()
st.dataframe(logs_df)


# ============================================================
# 🧠 END OF APPLICATION
# ============================================================
# Flow Summary:
# DB → Fetch → Detect → UI → User Action → Execute → Log → Display
# ============================================================

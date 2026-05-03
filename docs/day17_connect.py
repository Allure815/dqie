# ================================
# DAY 17 - PYTHON + POSTGRESQL
# FINAL WORKING FILE
# ================================

# Step 1: Import library
# This library allows Python to talk to PostgreSQL
import psycopg2


# Step 2: Try connecting to database
# We use try-except to catch errors safely
try:
    # Create connection object
    # This is like opening a connection between Python and DB
    conn = psycopg2.connect(
        dbname="db_pulse_lab",   # 👉 Replace with your DB name
        user="postgres",              # 👉 Default PostgreSQL user
        password="postgres123",     # 👉 Replace with your correct password
        host="localhost",             # 👉 DB is running on your system
        port="5432"                   # 👉 Default PostgreSQL port
    )

    print("✅ Connection successful\n")


    # Step 3: Create cursor
    # Cursor is used to send SQL queries
    cursor = conn.cursor()


    # ================================
    # STEP 4: FETCH ALL INCIDENTS
    # ================================

    print("📌 ALL INCIDENTS DATA:\n")

    # Run SQL query
    cursor.execute("SELECT * FROM incidents;")

    # Fetch all rows
    rows = cursor.fetchall()

    # Loop through rows
    for row in rows:
        print("Incident ID:", row[0])
        print("PID:", row[1])
        print("Query:", row[2])
        print("Duration:", row[3])
        print("Issue Type:", row[4])
        print("Root Cause:", row[5])
        print("Risk Score:", row[6])
        print("Recommendation:", row[7])
        print("Created Time:", row[8])
        print("-----------------------------")


    # ================================
    # STEP 5: RUN ANALYSIS QUERY (DAY 15)
    # ================================

    print("\n📊 ISSUE TYPE ANALYSIS:\n")

    cursor.execute("""
        SELECT issue_type, COUNT(*) 
        FROM incidents
        GROUP BY issue_type
        ORDER BY COUNT(*) DESC;
    """)

    analysis_rows = cursor.fetchall()

    for row in analysis_rows:
        print("Issue Type:", row[0], "| Count:", row[1])


    # ================================
    # STEP 6: RUN SUMMARY QUERY (DAY 16)
    # ================================

    print("\n🧠 SYSTEM SUMMARY:\n")

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

    summary = cursor.fetchone()

    print("Summary:", summary[0])


    # ================================
    # STEP 7: HIGH RISK SUMMARY
    # ================================

    print("\n⚠️ RISK SUMMARY:\n")

    cursor.execute("""
        SELECT 
        CASE
            WHEN COUNT(*) FILTER (WHERE risk_score >= 80) > 5
            THEN 'High number of critical issues detected'

            WHEN COUNT(*) FILTER (WHERE risk_score >= 80) > 0
            THEN 'Some critical issues detected'

            ELSE 'No critical issues, system stable'
        END
        FROM incidents;
    """)

    risk_summary = cursor.fetchone()

    print("Risk Status:", risk_summary[0])


    # ================================
    # STEP 8: CLOSE CONNECTION
    # ================================

    # Always close connection after work is done
    conn.close()

    print("\n🔒 Connection closed")


# ================================
# ERROR HANDLING
# ================================

except Exception as e:
    print("❌ ERROR OCCURRED:")
    print(e)# ================================
# DAY 17 - PYTHON + POSTGRESQL
# FINAL WORKING FILE
# ================================

# Step 1: Import library
# This library allows Python to talk to PostgreSQL
import psycopg2


# Step 2: Try connecting to database
# We use try-except to catch errors safely
try:
    # Create connection object
    # This is like opening a connection between Python and DB
    conn = psycopg2.connect(
        dbname="your_database_name",   # 👉 Replace with your DB name
        user="postgres",              # 👉 Default PostgreSQL user
        password="your_password",     # 👉 Replace with your correct password
        host="localhost",             # 👉 DB is running on your system
        port="5432"                   # 👉 Default PostgreSQL port
    )

    print("✅ Connection successful\n")


    # Step 3: Create cursor
    # Cursor is used to send SQL queries
    cursor = conn.cursor()


    # ================================
    # STEP 4: FETCH ALL INCIDENTS
    # ================================

    print("📌 ALL INCIDENTS DATA:\n")

    # Run SQL query
    cursor.execute("SELECT * FROM incidents;")

    # Fetch all rows
    rows = cursor.fetchall()

    # Loop through rows
    for row in rows:
        print("Incident ID:", row[0])
        print("PID:", row[1])
        print("Query:", row[2])
        print("Duration:", row[3])
        print("Issue Type:", row[4])
        print("Root Cause:", row[5])
        print("Risk Score:", row[6])
        print("Recommendation:", row[7])
        print("Created Time:", row[8])
        print("-----------------------------")


    # ================================
    # STEP 5: RUN ANALYSIS QUERY (DAY 15)
    # ================================

    print("\n📊 ISSUE TYPE ANALYSIS:\n")

    cursor.execute("""
        SELECT issue_type, COUNT(*) 
        FROM incidents
        GROUP BY issue_type
        ORDER BY COUNT(*) DESC;
    """)

    analysis_rows = cursor.fetchall()

    for row in analysis_rows:
        print("Issue Type:", row[0], "| Count:", row[1])


    # ================================
    # STEP 6: RUN SUMMARY QUERY (DAY 16)
    # ================================

    print("\n🧠 SYSTEM SUMMARY:\n")

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

    summary = cursor.fetchone()

    print("Summary:", summary[0])


    # ================================
    # STEP 7: HIGH RISK SUMMARY
    # ================================

    print("\n⚠️ RISK SUMMARY:\n")

    cursor.execute("""
        SELECT 
        CASE
            WHEN COUNT(*) FILTER (WHERE risk_score >= 80) > 5
            THEN 'High number of critical issues detected'

            WHEN COUNT(*) FILTER (WHERE risk_score >= 80) > 0
            THEN 'Some critical issues detected'

            ELSE 'No critical issues, system stable'
        END
        FROM incidents;
    """)

    risk_summary = cursor.fetchone()

    print("Risk Status:", risk_summary[0])


    # ================================
    # STEP 8: CLOSE CONNECTION
    # ================================

    # Always close connection after work is done
    conn.close()

    print("\n🔒 Connection closed")


# ================================
# ERROR HANDLING
# ================================

except Exception as e:
    print("❌ ERROR OCCURRED:")
    print(e)

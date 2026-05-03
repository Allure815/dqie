# ============================================================
# 🧠 DQIE - FINAL BACKEND (INTELLIGENCE + RECOMMENDATIONS)
# ============================================================

from fastapi import FastAPI, Query
import psycopg2
import pandas as pd

app = FastAPI()

# ============================================================
# 🧱 DB CONNECTION
# ============================================================

def get_connection():
    return psycopg2.connect(
        dbname="dqie_lab",
        user="postgres",
        password="postgres123",
        host="localhost",
        port="5432"
    )

# ============================================================
# 🧠 QUERY HISTORY (FEATURE 1)
# ============================================================

def update_query_history(query, duration, cur):
    cur.execute(
        "SELECT avg_duration, execution_count FROM query_history WHERE query = %s",
        (query,)
    )
    result = cur.fetchone()

    if result:
        old_avg, count = result
        new_avg = ((old_avg * count) + duration) / (count + 1)

        cur.execute("""
            UPDATE query_history
            SET avg_duration = %s,
                execution_count = %s,
                last_seen = CURRENT_TIMESTAMP
            WHERE query = %s
        """, (new_avg, count + 1, query))

        return old_avg
    else:
        cur.execute("""
            INSERT INTO query_history (query, avg_duration, execution_count)
            VALUES (%s, %s, %s)
        """, (query, duration, 1))

        return duration

# ============================================================
# ⚡ DYNAMIC RISK ENGINE (FEATURE 2)
# ============================================================

def calculate_dynamic_risk(duration, base_risk, anomaly, issue_type):
    risk = base_risk

    if duration > 100:
        risk += 15
    elif duration > 50:
        risk += 10
    elif duration > 20:
        risk += 5

    if anomaly:
        risk += 20

    if issue_type == "BLOCKING":
        risk += 15
    elif issue_type == "SLOW":
        risk += 5

    return min(risk, 100)

# ============================================================
# 💡 RECOMMENDATION ENGINE (FEATURE 3 🔥)
# ============================================================

def generate_recommendations(issue_type, duration, anomaly):
    recs = []

    if issue_type == "BLOCKING":
        recs.append("Kill blocking query immediately")
        recs.append("Check pg_locks for blocking sessions")
        recs.append("Investigate missing indexes")

    elif issue_type == "SLOW":
        recs.append("Use EXPLAIN ANALYZE to optimize query")
        recs.append("Add indexes on frequently filtered columns")
        recs.append("Avoid SELECT * in production")

    if duration > 100:
        recs.append("Investigate long-running transaction")
        recs.append("Check for full table scans")

    if anomaly:
        recs.append("Unusual spike detected — compare with historical runs")
        recs.append("Check recent deployments or schema changes")

    return recs

# ============================================================
# 📊 GET INCIDENTS
# ============================================================

@app.get("/incidents")
def get_incidents():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM incidents ORDER BY created_time DESC;", conn)
    conn.close()
    return df.to_dict(orient="records")

# ============================================================
# 🚨 GET CRITICAL QUERY
# ============================================================

@app.get("/critical")
def get_critical():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT pid, risk_score
        FROM incidents
        WHERE risk_score >= 80
        ORDER BY created_time DESC
        LIMIT 1;
    """)

    result = cur.fetchone()
    conn.close()

    if result:
        return {
            "pid": result[0],
            "risk_score": result[1],
            "status": "CRITICAL"
        }
    else:
        return {"status": "NO CRITICAL QUERY"}

# ============================================================
# ⚡ KILL QUERY + LOGGING
# ============================================================

@app.post("/kill_query")
def kill_query(pid: int):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(f"SELECT pg_terminate_backend({pid});")

        cur.execute("""
            INSERT INTO action_logs (action_type, target_pid, status)
            VALUES (%s, %s, %s)
        """, ("KILL_QUERY", pid, "SUCCESS"))

        conn.commit()
        conn.close()

        return {
            "status": "SUCCESS",
            "message": f"Query {pid} terminated"
        }

    except Exception as e:
        return {
            "status": "FAILED",
            "error": str(e)
        }

# ============================================================
# 📜 GET LOGS
# ============================================================

@app.get("/logs")
def get_logs():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM action_logs ORDER BY created_time DESC;", conn)
    conn.close()
    return df.to_dict(orient="records")

# ============================================================
# 🎭 SIMULATE SCENARIOS (FINAL INTELLIGENT VERSION)
# ============================================================

@app.post("/simulate")
def simulate(type: str = Query(...)):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM incidents")

    query = "N/A"
    duration = 0
    old_avg = 0
    anomaly = False
    risk = 0
    issue_type = "NORMAL"
    recommendations = []

    # 🐢 SLOW
    if type == "slow":
        query = "SELECT * FROM large_table"
        duration = 45
        issue_type = "SLOW"

        old_avg = update_query_history(query, duration, cur)
        anomaly = duration > (old_avg * 2)

        risk = calculate_dynamic_risk(duration, 50, anomaly, issue_type)
        recommendations = generate_recommendations(issue_type, duration, anomaly)

        cur.execute("""
            INSERT INTO incidents (pid, query, duration, issue_type, risk_score)
            VALUES (%s, %s, INTERVAL '45 seconds', %s, %s)
        """, (501, query, issue_type, risk))

    # 🚫 BLOCKING
    elif type == "blocking":
        query = "UPDATE users SET name = name"
        duration = 120
        issue_type = "BLOCKING"

        old_avg = update_query_history(query, duration, cur)
        anomaly = duration > (old_avg * 2)

        risk = calculate_dynamic_risk(duration, 70, anomaly, issue_type)
        recommendations = generate_recommendations(issue_type, duration, anomaly)

        cur.execute("""
            INSERT INTO incidents (pid, query, duration, issue_type, risk_score)
            VALUES (%s, %s, INTERVAL '120 seconds', %s, %s)
        """, (601, query, issue_type, risk))

    # ✅ RESET
    elif type == "normal":
        pass

    else:
        return {"status": "Invalid type"}

    conn.commit()
    conn.close()

    return {
        "status": "Scenario Applied",
        "type": type,
        "details": {
            "query": query,
            "duration": duration,
            "old_avg": old_avg,
            "anomaly": anomaly,
            "final_risk": risk,
            "recommendations": recommendations
        }
    }
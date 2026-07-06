# ============================================================
# 🧠 DQIE - FINAL BACKEND (INTELLIGENCE + RECOMMENDATIONS)
# ============================================================

from fastapi import FastAPI, Query
from pydantic import BaseModel
import psycopg2
import pandas as pd
import os
import google.generativeai as genai
from dotenv import load_dotenv
import json
from rag_engine import search_similar_incidents

app = FastAPI()
# ================================
# Gemini Configuration
# ================================

load_dotenv()

print("=" * 50)
print("API KEY:", os.getenv("GEMINI_API_KEY"))
print("=" * 50)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


model = genai.GenerativeModel("gemini-2.5-flash")

# ============================================================
# 🤖 AI SQL ANALYZER (FEATURE 4)
# ===========================================
# ============================================================
# 🤖 AI SQL ANALYZER (RAG + JSON OUTPUT FIXED)
# ============================================================

def analyze_sql_with_ai(query: str, duration: int):

    similar_incidents = search_similar_incidents(query)

    context = "\n".join([
        f"""
Previous Incident:
Query: {item['query']}
Issue: {item['issue']}
Solution: {item['solution']}
Improvement: {item['improvement']}
"""
        for item in similar_incidents
    ])

    prompt = f"""
You are a Senior PostgreSQL Database Performance Engineer.

Analyze the current SQL incident using BOTH:
1. Your PostgreSQL expertise.
2. Historical similar incidents.

===========================
Historical Incidents
===========================

{context}

===========================
Current Incident
===========================

SQL Query:
{query}

Execution Time:
{duration} seconds

Return ONLY valid JSON.

Use exactly this structure:

{{
    "root_cause": "...",
    "severity": "...",
    "business_impact": "...",
    "optimization": [
        "...",
        "...",
        "..."
    ],
    "expected_improvement": "...",
    "confidence": "..."
}}

Rules:
- Do NOT use markdown
- Do NOT wrap in ``` blocks
- Return ONLY JSON
"""

    try:
        response = model.generate_content(prompt)

        clean_text = (
            response.text
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        return json.loads(clean_text)

    except Exception as e:
        return {
            "root_cause": "AI analysis failed or invalid JSON.",
            "severity": "Error",
            "business_impact": str(e),
            "optimization": [],
            "expected_improvement": "Unknown",
            "confidence": "Low"
        }


# ============================================================
# 🤖 AI SQL EXPLAINER (TEXT OUTPUT)
# ============================================================

def explain_sql_with_ai(query: str):

    prompt = f"""
You are a Senior PostgreSQL Database Performance Engineer.

Analyze the following SQL query.

SQL Query:
{query}

Provide:

Purpose:
Tables Involved:
Potential Performance Issues:
Optimization Suggestions:

Keep it concise and technical.
"""

    try:
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"SQL Explanation Failed: {str(e)}"

# ============================================================
# 🤖 AI DBA COPILOT
# ============================================================

def dba_copilot(question: str, query: str):

    similar = search_similar_incidents(query)

    context = "\n".join([
        f"""
Previous Incident
Query: {item['query']}
Issue: {item['issue']}
Solution: {item['solution']}
Improvement: {item.get('improvement','N/A')}
"""
        for item in similar
    ])

    prompt = f"""
You are an expert PostgreSQL Database Administrator.

You are helping a DBA troubleshoot a production issue.

Current SQL Query:

{query}

Similar Historical Incidents:

{context}

User Question:

{question}

Answer professionally.

Use bullet points whenever appropriate.

Be concise.

Give practical DBA advice.

If possible, refer to previous incidents.
"""

    try:

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:

        return f"Copilot Error: {e}"
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
    ai_analysis = "No AI analysis available."
    sql_explanation = ""
    similar_incidents = []

    # 🐢 SLOW
    if type == "slow":
        query = "SELECT * FROM large_table"
        duration = 45
        issue_type = "SLOW"

        old_avg = update_query_history(query, duration, cur)
        anomaly = duration > (old_avg * 2)

        risk = calculate_dynamic_risk(duration, 50, anomaly, issue_type)

        recommendations = generate_recommendations(
            issue_type,
            duration,
            anomaly
        )

        # 🤖 AI Analysis
        ai_analysis = analyze_sql_with_ai(query, duration)
        sql_explanation = explain_sql_with_ai(query)
        similar_incidents = search_similar_incidents(query)

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

        recommendations = generate_recommendations(
            issue_type,
            duration,
            anomaly
        )

        # 🤖 AI Analysis
        ai_analysis = analyze_sql_with_ai(query, duration)
        sql_explanation = explain_sql_with_ai(query)
        similar_incidents = search_similar_incidents(query)

        cur.execute("""
            INSERT INTO incidents (pid, query, duration, issue_type, risk_score)
            VALUES (%s, %s, INTERVAL '120 seconds', %s, %s)
        """, (601, query, issue_type, risk))

    # ✅ RESET
    elif type == "normal":
        pass

    else:
        conn.close()
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
    		"recommendations": recommendations,
    		"ai_analysis": ai_analysis,
                "sql_explanation": sql_explanation,
                "similar_incidents": similar_incidents
		}
    }

# ============================================================
# 🤖 AI DBA COPILOT ENDPOINT
# ============================================================

class CopilotRequest(BaseModel):
    question: str
    query: str


@app.post("/copilot")
def ai_dba_copilot(request: CopilotRequest):

    answer = dba_copilot(
        request.question,
        request.query
    )

    return {
        "answer": answer
    }
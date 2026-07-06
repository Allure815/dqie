
# 🧠 DQIE - FINAL STREAMLIT UI (STABLE + INTELLIGENT)
# ============================================================

import streamlit as st
import requests
import pandas as pd

# ============================================================
# 🌐 API CONFIG
# ============================================================

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="DQIE", layout="wide")

# ============================================================
# 🧠 SESSION STATE INIT (IMPORTANT FIX)
# ============================================================

if "details" not in st.session_state:
    st.session_state.details = None

# ============================================================
# 🏷️ HEADER
# ============================================================

from datetime import datetime

st.title("🧠 DQIE")
st.subheader("Database Intelligence Copilot")

st.caption(
    "Enterprise AI for PostgreSQL Monitoring • Root Cause Analysis • Performance Optimization"
)

left, middle, right = st.columns([6, 2, 2])

with left:
    st.markdown("### 📡 Live Database Intelligence Dashboard")

with middle:
    st.success("🟢 Connected")

with right:
    st.caption("Last Refresh")
    st.write(datetime.now().strftime("%H:%M:%S"))

st.markdown("---")

# ============================================================
# 🗄️ DATABASE CONTROLS
# ============================================================

st.header("🗄️ Database Controls")
st.caption(
    "Generate database events to observe DQIE's AI-powered diagnostics and performance analysis."
)

control1, control2, control3 = st.columns(3)

# 🐢 Slow Query
with control1:
    if st.button("🐢 Slow Query", use_container_width=True):
        res = requests.post(f"{API_URL}/simulate", params={"type": "slow"})
        if res.status_code == 200:
            st.session_state.details = res.json().get("details")

# 🚫 Blocking Query
with control2:
    if st.button("🚫 Blocking Query", use_container_width=True):
        res = requests.post(f"{API_URL}/simulate", params={"type": "blocking"})
        if res.status_code == 200:
            st.session_state.details = res.json().get("details")

# ✅ Reset
with control3:
    if st.button("✅ Reset System", use_container_width=True):
        requests.post(f"{API_URL}/simulate", params={"type": "normal"})
        st.session_state.details = None

details = st.session_state.details

st.markdown("---")

# ============================================================
# 🧠 INTELLIGENCE OVERVIEW
# ============================================================

if details:

    st.header("🧠 Intelligence Overview")
    st.caption(
        "Real-time performance metrics generated from the latest database workload."
    )

    metric1, metric2, metric3 = st.columns(3)

    with metric1:
        st.metric(
            label="⏱ Query Duration",
            value=f"{details.get('duration', 0)} sec"
        )

    with metric2:
        st.metric(
            label="📊 Historical Average",
            value=f"{round(details.get('old_avg', 0), 2)} sec"
        )

    with metric3:
        risk = details.get("final_risk", 0)

        st.metric(
            label="🔥 Risk Score",
            value=f"{risk}/100"
        )

        st.progress(min(risk / 100, 1.0))

    st.markdown("---")

    st.markdown("### 📝 Executed SQL Query")
    st.code(details.get("query", "N/A"), language="sql")

    st.markdown("### 🚦 Workload Status")

    if details.get("anomaly"):
        st.error("🚨 Anomaly Detected — The observed query behavior deviates from historical patterns.")
    else:
        st.success("✅ Normal Pattern — Query execution is consistent with historical behavior.")

    st.markdown("### 📊 Risk Assessment Factors")

    st.info(
        """
**DQIE evaluates risk using multiple indicators:**

- ⏱ Query execution duration
- 📊 Historical workload comparison
- 🚫 Blocking activity detection
- 🤖 AI-based anomaly analysis
"""
    )

else:
    st.info("Run a database workload to generate performance insights.")


# ============================================================
# ============================================================
# 🤖 AI ROOT CAUSE ANALYSIS
# ============================================================

st.header("🤖 AI Root Cause Analysis")
st.caption(
    "AI-generated diagnosis and recommendations based on the latest database workload."
)

if details:

    with st.container(border=True):

        ai = details.get("ai_analysis")

        if ai and isinstance(ai, dict):

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### 🚨 Root Cause")
                st.error(ai.get("root_cause", "N/A"))

            with col2:
                st.markdown("#### 🔥 Severity")
                st.warning(ai.get("severity", "N/A"))

            st.markdown("---")

            info1, info2 = st.columns(2)

            with info1:
                st.markdown("#### 💼 Business Impact")
                st.info(ai.get("business_impact", "N/A"))

            with info2:
                st.markdown("#### 📈 Expected Improvement")
                st.success(ai.get("expected_improvement", "N/A"))

            st.markdown("---")

            confidence = ai.get("confidence", "N/A")

            st.metric(
                label="🎯 AI Confidence",
                value=confidence
            )

            st.markdown("---")

            st.markdown("### 💡 Recommended Optimizations")

            for item in ai.get("optimization", []):
                st.markdown(f"✅ {item}")

        else:
            st.warning("No AI analysis available.")

else:
    st.info("Run a query to generate AI analysis.")

# ============================================================
# 📘 AI SQL EXPLANATION
# ============================================================

st.markdown("---")

st.header("📘 AI SQL Explanation")
st.caption(
    "Natural language explanation of the detected SQL query generated by DQIE AI."
)

if details:

    sql_text = details.get("sql_explanation")

    if sql_text:

        with st.container(border=True):
            st.success(sql_text)

    else:
        st.warning("No SQL explanation available.")

else:
    st.info("Run a query to generate SQL explanation.")
# ============================================================
# ============================================================
# 🧠 INCIDENT KNOWLEDGE BASE
# ============================================================

st.markdown("---")

st.header("🧠 Incident Knowledge Base")
st.caption(
    "Semantic retrieval of historical incidents using vector similarity to recommend proven resolutions."
)

if details:

    similar = details.get("similar_incidents", [])

    if len(similar) > 0:

        st.success(
            f"✅ {len(similar)} relevant historical incident(s) matched using semantic search."
        )

        for i, incident in enumerate(similar, start=1):

            similarity = incident.get("similarity", 0)

            st.markdown("---")

            with st.expander(
                f"📄 Incident #{i}  |  🎯 Similarity: {similarity}%",
                expanded=(i == 1)
            ):

                st.metric(
                    "🎯 Similarity Score",
                    f"{similarity}%"
                )

                st.markdown("### 📝 Historical SQL Query")

                st.code(
                    incident.get("query", "N/A"),
                    language="sql"
                )

                st.markdown("### 🚨 Observed Issue")

                st.warning(
                    incident.get("issue", "N/A")
                )

                st.markdown("### ✅ Recommended Resolution")

                st.success(
                    incident.get("solution", "N/A")
                )

                if incident.get("improvement"):

                    st.markdown("### 📈 Performance Improvement")

                    st.info(
                        incident.get("improvement")
                    )

                if incident.get("distance") is not None:

                    st.caption(
                        f"Semantic Distance: {incident.get('distance')}"
                    )

    else:

        st.info(
            "No semantically similar historical incidents were found in the knowledge base."
        )

else:

    st.info(
        "Run a query to search the incident knowledge base."
    )

st.markdown("---")
# ============================================================
# ============================================================
# 📊 INCIDENT OPERATIONS
# ============================================================

st.header("📊 Incident Operations")
st.caption(
    "Historical database incidents collected and analyzed by DQIE."
)

try:
    res = requests.get(f"{API_URL}/incidents", timeout=5)

    if res.status_code == 200:
        data = res.json()

        if data:

            df = pd.DataFrame(data)

            df.columns = [
                col.replace("_", " ").title()
                for col in df.columns
            ]

            st.info(f"📈 Total Incidents Retrieved: {len(df)}")

            with st.container(border=True):

                try:

                    if "Risk Score" in df.columns:

                        st.dataframe(
                            df.style.background_gradient(
                                subset=["Risk Score"],
                                cmap="Reds"
                            ),
                            use_container_width=True,
                            hide_index=True
                        )

                    else:

                        st.dataframe(
                            df,
                            use_container_width=True,
                            hide_index=True
                        )

                except Exception:

                    st.dataframe(
                        df,
                        use_container_width=True,
                        hide_index=True
                    )

        else:
            st.info("No incidents found.")

    else:
        st.error("Failed to fetch incidents.")

except Exception as e:
    st.error(f"API error: {e}")

st.markdown("---")

# ============================================================
# 🚨 CRITICAL QUERY MONITOR
# ============================================================

st.header("🚨 Critical Query Monitor")
st.caption(
    "Continuously monitors active workloads for high-risk database queries."
)

try:

    res = requests.get(f"{API_URL}/critical", timeout=60)

    if res.status_code == 200:

        critical = res.json()

        if critical.get("status") == "CRITICAL":

            pid = critical["pid"]
            risk = critical["risk_score"]

            st.error(
                f"🚨 High-Risk Query Detected\n\n"
                f"**PID:** {pid} | **Risk Score:** {risk}"
            )

            if st.button(
                "⚡ Kill Query",
                use_container_width=True
            ):

                kill = requests.post(
                    f"{API_URL}/kill_query",
                    params={"pid": pid}
                )

                result = kill.json()

                if result.get("status") == "SUCCESS":

                    st.success(result.get("message"))

                else:

                    st.error(result.get("error"))

        else:

            st.success("✅ No critical queries detected. Database is operating normally.")

    else:

        st.error("Failed to check critical queries.")

except Exception as e:

    st.error(f"API error: {e}")

st.markdown("---")
# ============================================================
# 📜 OPERATIONAL ACTIVITY
# ============================================================

st.header("📜 Operational Activity")
st.caption(
    "Chronological record of automated database actions and DQIE system events."
)

try:

    res = requests.get(f"{API_URL}/logs", timeout=5)

    if res.status_code == 200:

        logs = res.json()

        if logs:

            df_logs = pd.DataFrame(logs)

            df_logs.columns = [
                col.replace("_", " ").title()
                for col in df_logs.columns
            ]

            st.info(f"📝 Total Log Entries: {len(df_logs)}")

            with st.container(border=True):

                st.dataframe(
                    df_logs,
                    use_container_width=True,
                    hide_index=True
                )

        else:

            st.info("No operational logs available.")

    else:

        st.error("Failed to fetch logs.")

except Exception as e:

    st.error(f"API error: {e}")

# ============================================================
# 🤖 AI DBA COPILOT
# ============================================================

st.markdown("---")

st.header("🤖 AI DBA Copilot")
st.caption(
    "Ask DQIE AI questions about the current database workload and receive intelligent recommendations."
)

if details:

    with st.container(border=True):

        user_question = st.text_input(
            "💬 Ask your database question",
            placeholder="Example: Which columns should be indexed?"
        )

        if st.button(
            "🚀 Ask Copilot",
            use_container_width=True
        ):

            if user_question.strip():

                with st.spinner("🤖 DQIE AI is analyzing your request..."):

                    payload = {
                        "question": user_question,
                        "query": details.get("query", "")
                    }

                    response = requests.post(
                        f"{API_URL}/copilot",
                        json=payload
                    )

                    if response.status_code == 200:

                        answer = response.json()["answer"]

                        st.markdown("### 🤖 Copilot Response")

                        st.success(answer)

                    else:

                        st.error("Failed to contact AI Copilot.")

else:

    st.info(
        "Execute a database workload first, then ask DQIE AI about the detected query."
    )
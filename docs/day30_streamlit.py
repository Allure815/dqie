# ============================================================
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
# 🏷️ HEADER
# ============================================================

st.title("🧠 DB Query Intelligence Engine")
st.markdown("### ⚠️ Simulated Demo System")

# ============================================================
# 🎭 DEMO CONTROLS
# ============================================================

st.subheader("🎭 Demo Controls")

col1, col2, col3 = st.columns(3)

details = None

# 🐢 SLOW
with col1:
    if st.button("🐢 Slow Query"):
        res = requests.post(f"{API_URL}/simulate", params={"type": "slow"})
        if res.status_code == 200:
            details = res.json().get("details")

# 🚫 BLOCKING
with col2:
    if st.button("🚫 Blocking Query"):
        res = requests.post(f"{API_URL}/simulate", params={"type": "blocking"})
        if res.status_code == 200:
            details = res.json().get("details")

# ✅ RESET
with col3:
    if st.button("✅ Reset System"):
        requests.post(f"{API_URL}/simulate", params={"type": "normal"})
        details = None

# ============================================================
# 🧠 INTELLIGENCE PANEL (🔥 YOUR USP)
# ============================================================

if details:
    st.markdown("---")
    st.subheader("🧠 Intelligence Breakdown")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("⏱ Duration (sec)", details.get("duration"))

    with c2:
        st.metric("📊 Historical Avg", round(details.get("old_avg", 0), 2))

    with c3:
        st.metric("🔥 Final Risk", details.get("final_risk"))

    st.write(f"**Query:** `{details.get('query')}`")

    # 🚨 ANOMALY DETECTION
    if details.get("anomaly"):
        st.error("🚨 Anomaly Detected (Unusual Behavior)")
    else:
        st.success("✅ Normal Pattern")

    st.markdown("### 📊 Why this risk?")
    st.write("""
    - Duration impacts system performance  
    - Compared with historical behavior  
    - Blocking queries increase severity  
    """)

st.markdown("---")

# ============================================================
# 📊 INCIDENTS TABLE
# ============================================================

st.subheader("📊 Incidents")

try:
    res = requests.get(f"{API_URL}/incidents", timeout=5)

    if res.status_code == 200:
        data = res.json()

        if data:
            df = pd.DataFrame(data)

            df.columns = [col.replace("_", " ").title() for col in df.columns]

            # ✅ SAFE GRADIENT (NO CRASH)
            try:
                if "Risk Score" in df.columns:
                    st.dataframe(
                        df.style.background_gradient(
                            subset=["Risk Score"],
                            cmap="Reds"
                        ),
                        use_container_width=True
                    )
                else:
                    st.dataframe(df, use_container_width=True)

            except Exception:
                # fallback if matplotlib missing
                st.dataframe(df, use_container_width=True)

        else:
            st.info("No incidents found")

    else:
        st.error("Failed to fetch incidents")

except Exception as e:
    st.error(f"API error: {e}")

st.markdown("---")

# ============================================================
# 🚨 CRITICAL DETECTION
# ============================================================

st.subheader("🚨 Critical Detection")

try:
    res = requests.get(f"{API_URL}/critical", timeout=5)

    if res.status_code == 200:
        critical = res.json()

        if critical.get("status") == "CRITICAL":
            pid = critical["pid"]
            risk = critical["risk_score"]

            st.warning(f"⚠️ Critical Query Found | PID: {pid} | Risk: {risk}")

            if st.button("⚡ Kill Query"):
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
            st.success("✅ System Stable")

    else:
        st.error("Failed to check critical queries")

except Exception as e:
    st.error(f"API error: {e}")

st.markdown("---")

# ============================================================
# 📜 ACTION LOGS
# ============================================================

st.subheader("📜 Action Logs")

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

            st.dataframe(df_logs, use_container_width=True)

        else:
            st.info("No logs available")

    else:
        st.error("Failed to fetch logs")

except Exception as e:
    st.error(f"API error: {e}")

# ============================================================
# 🧠 END
# ============================================================
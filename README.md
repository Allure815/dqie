# 🧠 DQIE — Database Intelligence Copilot

> AI-powered PostgreSQL Observability, Root Cause Analysis, Semantic Incident Search & Intelligent DBA Assistant

# 📌 Overview

DQIE (Database Intelligence Copilot) is an AI-powered database observability platform that combines traditional PostgreSQL monitoring with Large Language Models (LLMs) and Retrieval-Augmented Generation (RAG) to help Database Administrators rapidly diagnose performance issues, understand SQL queries, retrieve similar historical incidents, and receive AI-generated optimization recommendations.

Instead of manually investigating slow queries, blocking sessions, execution plans, and historical tickets, DQIE provides intelligent diagnostics through an interactive AI dashboard.

---

# 🎥 Demo

## 📺 Project Walkthrough

👉 **Demo Video**

> ****

---

# 📸 Screenshots

## Dashboard

![Dashboard](https://github.com/Allure815/dqie/blob/main/demo/Dashboard.png)

---

## AI Root Cause Analysis

![AI RCA](https://github.com/Allure815/dqie/blob/main/demo/RCA.png)

---

## Semantic Incident Search

![Semantic Search](https://github.com/Allure815/dqie/blob/main/demo/Semantic%20Search-1.png)


---

**##Other Functionalities**

https://github.com/Allure815/dqie/blob/main/demo/Other.png
---

## AI DBA Copilot

![Copilot](https://github.com/Allure815/dqie/blob/main/demo/Copilot.png)

---

# 🚀 Features

## 📊 Database Monitoring

- PostgreSQL workload monitoring
- Query performance metrics
- Historical performance comparison
- Risk scoring engine
- Incident tracking
- Operational activity logs

---

## 🧠 AI Root Cause Analysis

Automatically analyzes database issues and provides

- Root Cause
- Severity
- Business Impact
- Expected Improvement
- AI Confidence Score
- Optimization Recommendations

Powered using Google Gemini.

---

## 📘 AI SQL Explainer

Explains SQL queries in simple English.

Useful for:

- Junior DBAs
- Developers
- SQL learners
- Interview preparation

---

## 🔍 Semantic Incident Search (RAG)

Uses FAISS vector search to retrieve similar historical incidents instead of keyword matching.

Returns:

- Similar SQL query
- Previous issue
- Previous resolution
- Performance improvement
- Similarity score

---

## 🤖 AI DBA Copilot

Interactive AI assistant capable of answering questions such as:

- Why is this query slow?
- Which columns should be indexed?
- How can I reduce execution time?
- Why is CPU utilization high?
- What optimization strategy should I use?

---

## 🚨 Critical Query Detection

Automatically identifies high-risk database workloads.

Supports:

- Risk threshold monitoring
- Query identification
- Manual termination (Kill Query)
- Live dashboard alerts

---

## 📈 Interactive Dashboard

Built using Streamlit with

- Real-time metrics
- Risk visualization
- SQL formatting
- Incident explorer
- AI insights
- Responsive enterprise-style interface

---

# 🏗️ Architecture

```
                    PostgreSQL Database
                           │
                           │
                    Performance Metrics
                           │
                           ▼
                 FastAPI Backend Services
                           │
     ┌──────────────┬──────────────┬──────────────┐
     │              │              │
     ▼              ▼              ▼
 Risk Engine     Gemini AI      RAG Engine
                     │             │
                     ▼             ▼
              AI Analysis     FAISS Search
                     │             │
                     └──────┬──────┘
                            ▼
                 Streamlit Dashboard
                            │
                            ▼
                       End User
```

---

# 🛠️ Tech Stack

## Backend

- Python
- FastAPI

## Frontend

- Streamlit

## Database

- PostgreSQL

## AI

- Google Gemini API
- Prompt Engineering

## RAG

- FAISS
- Vector Embeddings
- Semantic Search

## Data Processing

- Pandas

---

# 📂 Project Structure

```
DQIE/

│
├── database/
├── demo/
├── docs/
│
├── day30_api.py
├── day30_streamlit.py
├── rag_engine.py
├── knowledge_base.json
├── README.md
└── requirements.txt
```

---

# ⚙️ Installation

Clone repository

```bash
git clone https://github.com/Allure815/DQIE.git
```

Go into project

```bash
cd DQIE/docs
```

Install packages

```bash
pip install -r requirements.txt
```

Run FastAPI

```bash
uvicorn day30_api:app --reload
```

Run Streamlit

```bash
streamlit run day30_streamlit.py
```

---

# 💡 Example Workflow

1. Launch DQIE Dashboard
2. Generate database workload
3. Analyze SQL query
4. Review AI Root Cause Analysis
5. Search similar incidents using semantic search
6. Receive optimization recommendations
7. Ask AI DBA Copilot follow-up questions

---

# 📊 Key Capabilities

✅ AI Root Cause Analysis

✅ SQL Explanation

✅ Semantic Incident Retrieval

✅ Vector Search

✅ Intelligent Risk Scoring

✅ AI DBA Copilot

✅ Query Optimization Suggestions

✅ PostgreSQL Monitoring

✅ Incident Management

✅ Enterprise Dashboard

---

# 🔮 Future Enhancements

- Live PostgreSQL Monitoring
- Multi-database support (Oracle, SQL Server, MySQL)
- Predictive failure detection
- Automated indexing recommendations
- Grafana integration
- Docker deployment
- Kubernetes deployment
- User authentication
- REST API documentation
- Multi-user support

---

# 👩‍💻 About Me

**Heeral Madlani**

AI & Data Systems Engineer | Database Engineer | AI Enthusiast

- PostgreSQL
- FastAPI
- Streamlit
- Generative AI
- RAG
- FAISS
- LLM Applications
- Python


GitHub:
https://github.com/Allure815

---


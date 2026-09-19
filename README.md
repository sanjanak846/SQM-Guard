# 🛡️ SQM-Guard

**An AI-powered SOC automation platform with self-repairing query generation, prompt-injection defense, and MITRE ATT&CK-based multi-stage attack correlation.**

Built as a research-grounded improvement over *"Toward Autonomous SOC Operations: End-to-End LLM Framework for Threat Detection, Query Generation, and Resolution in Security Operations"* (Sajut & Azim, PMLR, 2026).

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688)
![React](https://img.shields.io/badge/React-Frontend-61DAFB)
![Ollama](https://img.shields.io/badge/LLM-Ollama%20(Local)-black)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🎯 What it does

SQM-Guard is an AI-driven SOC copilot that automates the three most time-consuming parts of security alert triage:

1. **Detects** which alerts are genuinely critical using a hybrid classical ML + LLM ensemble
2. **Generates and self-verifies** the SIEM investigation query for each alert (with a closed-loop repair mechanism)
3. **Recommends a resolution** with a clear, auditable justification — always subject to human approval

Unlike the base research framework it improves on, SQM-Guard also:
- 🛡️ **Defends against prompt injection** — attackers hiding instructions inside log fields to manipulate the AI
- 🔗 **Correlates multi-stage attacks** — linking related alerts into a single MITRE ATT&CK-mapped campaign instead of isolated tickets
- ✅ **Enforces human approval** — every AI recommendation requires analyst sign-off before closure, with a full audit trail

---

## 🏗️ Architecture

```
Raw SIEM Logs
     │
     ▼
Field Sanitizer + Injection Defense Layer
     │
     ▼
Detection Engine (Classical ML + LLM Ensemble)
     │
     ├──────────────► Entity Graph + MITRE ATT&CK Correlation ──► Campaign Detection
     │
     ▼
SQM Engine — Query Generation + Self-Repair Loop
     │
     ▼
Risk Scoring + Resolution Recommendation (RAG-grounded)
     │
     ▼
Human Approval Workflow (full audit trail)
     │
     ▼
Analyst Dashboard (React)
```

---

## 📊 Evaluation Results

| Metric | Result |
|---|---|
| Injection defense catch rate | 7/7 malicious test cases (100%) |
| False positives (injection defense) | 0 |
| Query generation — first-try executable rate | 73.3% |
| Query generation — final executable rate (with self-repair) | 80.0% |
| Multi-stage campaign correlation | Correctly grouped linked alerts; correctly excluded unrelated ones |

*Full methodology and honest limitations discussed in [`eval/results.md`](eval/results.md).*

---

## 🖥️ Screenshots

*(Add 3-4 screenshots here: Alert Queue, Alert Detail with risk breakdown, Campaign View — see setup instructions below)*

```
![Alert Queue](docs/screenshots/alert-queue.png)
![Alert Detail](docs/screenshots/alert-detail.png)
![Campaign View](docs/screenshots/campaign-view.png)
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, FastAPI, SQLAlchemy, SQLite |
| AI / LLM | Ollama (Llama 3.1 8B / TinyLlama), LangChain |
| Retrieval | ChromaDB, sentence-transformers |
| ML | scikit-learn (Isolation Forest) |
| Correlation | NetworkX (entity graph + MITRE ATT&CK sequencing) |
| Frontend | React, React Router, Axios |
| Deployment | Docker, Docker Compose |

---

## 🚀 Setup

### Prerequisites
- Python 3.11+
- Node.js (LTS)
- [Ollama](https://ollama.com) installed locally

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/sqm-guard.git
cd sqm-guard
```

### 2. Backend setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac/Linux
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Backend runs at `http://127.0.0.1:8000` — API docs at `/docs`.

### 3. Frontend setup
```bash
cd frontend
npm install
npm start
```
Dashboard runs at `http://localhost:3000`.

### 4. Pull the local LLM
```bash
ollama pull llama3.1:8b
```

### 5. (Optional) Run with Docker
```bash
docker-compose up --build
```

---

## 📁 Project Structure

```
sqm-guard/
├── backend/
│   ├── app/
│   │   ├── routers/          # API endpoints
│   │   ├── services/         # Detection, sanitizer, SQM engine, risk scoring, correlation
│   │   ├── models.py         # Database schema
│   │   └── main.py
│   ├── eval/                 # Evaluation scripts and results
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── pages/            # Alert Queue, Alert Detail, Campaign View
│       └── api/
├── dataset/                  # Sample logs, MITRE ATT&CK data, injection test cases
├── docs/                     # Architecture diagrams, screenshots, technical report
├── docker-compose.yml
└── README.md
```

---

## 📚 Research Foundation

This project is built as an evidence-based improvement over five key papers, identifying and closing specific gaps rather than reinventing the field:

1. Sajut & Azim (2026) — *Toward Autonomous SOC Operations* — base framework
2. Pandey & Bhujang (2026) — *Poisoning the Watchtower* — log-substrate prompt injection, motivates the defense layer
3. Wang et al. (2026) — *Landscape of Prompt Injection Threats in LLM Agents* — broader threat taxonomy
4. Chen et al. (2023) — *Teaching LLMs to Self-Debug* — foundation for the query self-repair loop
5. Deng et al. (2025) — *ReFoRCE* — error-categorization approach adapted for KQL repair

Full literature review and gap analysis in [`docs/technical_report.md`](docs/technical_report.md).

---

## 👥 Team

Built by **Sanjana K** and **Yuvasri S**, B.Tech CSE (Cyber Security), VIT Vellore.

## ⚠️ Disclaimer

This is an academic project built for educational and portfolio purposes. It is not intended for production security use without significant further hardening, testing at scale, and professional security review.

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

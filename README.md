# 🚀 Backup Failure Triage Agent

> **AI-Powered Multi-Agent System for Automated Infrastructure Incident Analysis**

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Google Gemini](https://img.shields.io/badge/Google-Gemini-orange)
![Google ADK](https://img.shields.io/badge/Google-ADK-green)
![License](https://img.shields.io/badge/License-MIT-blue)
![Status](https://img.shields.io/badge/Status-v1.0-success)

---

## 📌 Overview

Backup Failure Triage Agent is an AI-powered multi-agent system that automates infrastructure incident analysis.

Instead of manually reading backup logs, identifying the root cause, writing remediation steps, and creating incident reports, this application performs the complete workflow using Google Gemini and multiple AI agents.

The project is designed for:

- Managed Service Providers (MSPs)
- Infrastructure Engineers
- Backup Administrators
- DevOps Engineers
- Site Reliability Engineers (SRE)
- Cloud Operations Teams

---

## 🎯 Problem Statement

Backup failures require engineers to:

- Review lengthy logs
- Identify the root cause
- Determine remediation
- Write incident reports
- Create recovery scripts

This process is repetitive, time-consuming, and depends heavily on engineer experience.

The Backup Failure Triage Agent automates these tasks using AI.

---

# 🏗 Architecture

```
                    Input Log
                         │
                         ▼
                Incident Analysis Agent
                         │
                         ▼
                Remediation Agent
                         │
                         ▼
                  Report Agent
                         │
                         ▼
                    Coordinator
                         │
        ┌────────────────┴───────────────┐
        ▼                                ▼
 Markdown Incident Report      PowerShell Script
```

---

# ⚙ Workflow

```
Backup Log
      │
      ▼
Log Parser
      │
      ▼
Log Sanitizer
      │
      ▼
Incident Analysis Agent
      │
      ▼
Google Gemini
      │
      ▼
Structured Incident
      │
      ▼
Remediation Agent
      │
      ▼
Google Gemini
      │
      ▼
Remediation Plan
      │
      ▼
Report Agent
      │
      ▼
Markdown Report
      │
      ▼
PowerShell Script
```

---

# 📂 Project Structure

```
Backup_Triage/

├── agents/
├── cli/
├── config/
├── core/
├── data/
│   └── sample_logs/
├── docs/
├── logs/
├── mcp_server/
├── memory/
├── models/
├── output/
├── prompts/
├── reports/
├── scripts/
├── services/
├── tests/
├── tools/

├── .env.example
├── README.md
├── requirements.txt
├── pyproject.toml
├── run.py
├── adk_runner.py
```

---

# 🤖 AI Agents

## 1️⃣ Incident Analysis Agent

Responsible for:

- Parsing logs
- Sanitizing sensitive information
- Calling Gemini
- Identifying root cause
- Producing structured Incident objects

---

## 2️⃣ Remediation Agent

Responsible for:

- Understanding the incident
- Generating remediation
- Producing PowerShell scripts
- Estimating risk level

---

## 3️⃣ Report Agent

Responsible for:

- Combining incident and remediation
- Creating executive summaries
- Producing MSP-ready incident reports

---

## 4️⃣ Coordinator

Responsible for orchestrating the complete workflow.

---

# 🚀 Features

- AI-powered incident analysis
- Multi-Agent architecture
- Google Gemini integration
- Google ADK wrappers
- Log sanitization
- Structured Pydantic models
- Prompt management
- Markdown report generation
- PowerShell remediation generation
- Extensible architecture

---

# 🛠 Technologies

- Python
- Google Gemini
- Google ADK
- Pydantic
- Python Logging
- Markdown
- PowerShell

---

# 📥 Installation

Clone the repository.

```bash
git clone https://github.com/YOUR_USERNAME/Backup-Failure-Triage-Agent.git

cd Backup-Failure-Triage-Agent
```

Create a virtual environment.

```bash
python -m venv venv
```

Activate it.

Windows

```bash
venv\Scripts\activate
```

Linux

```bash
source venv/bin/activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

---

# 🔑 Configure Environment

Create a `.env` file.

```
GEMINI_API_KEY=YOUR_API_KEY

GEMINI_MODEL=gemini-2.5-flash

LOG_LEVEL=INFO

ENABLE_LOG_SANITIZATION=True
```

---

# 📁 Sample Logs

Store logs inside:

```
data/sample_logs/
```

Supported in Version 1:

- Repository Full
- Network Timeout
- Snapshot Failure
- Credential Failure
- Agent Offline

---

# ▶ Running the Project

```bash
python adk_runner.py data/sample_logs/repository_full.log
```

---

# ✅ Expected Output

The application generates:

- Incident Analysis
- Root Cause
- Remediation Plan
- PowerShell Script
- Markdown Incident Report

---

# 📄 Output Files

```
reports/generated/

scripts/powershell/

logs/
```

---

# 📈 Future Roadmap

Version 2 will include:

- Windows Event Viewer Support
- VMware Support
- Hyper-V Support
- Linux Syslogs
- Azure Backup
- AWS Backup
- Docker Logs
- Kubernetes Logs
- RAG Integration
- ChromaDB Memory
- MCP Server
- Streamlit Dashboard

---

# 🧪 Validation Checklist

- Incident generated successfully
- Remediation generated
- Report generated
- Markdown saved
- PowerShell saved
- No validation errors

---

# 📸 Screenshots

<img width="1350" height="899" alt="image" src="https://github.com/user-attachments/assets/b60a17a7-4c55-494d-87e3-e2b7b8ee85d9" />

<img width="1356" height="902" alt="image" src="https://github.com/user-attachments/assets/fb2b3fb0-7d5a-43da-9633-828442cae083" />

---

# 🎥 Demo

YouTube: https://studio.youtube.com/video/UthHUXJ8JsI/edit

---

# 📚 Kaggle Submission

This project was developed for the

**Google AI Agents Intensive Vibe Coding Course**

Track:

**Agents for Business**

---

# 👨‍💻 Author

**Mahesh Kolekar**

- AI Engineer
- Infrastructure & Backup Specialist
- Python Developer
- Google AI Agents Intensive Course Participant

---

# 📄 License

MIT License

---

# ⭐ If you found this project useful, consider giving it a Star!

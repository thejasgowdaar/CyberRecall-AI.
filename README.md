# 🛡️ CyberRecall AI
### AI-Powered Cybersecurity Incident Response Agent

**CyberRecall AI** is an intelligent cybersecurity incident response system designed to help security teams investigate incidents faster by combining AI-powered threat analysis with historical incident memory.

Instead of analysing every security incident in isolation, CyberRecall AI uses historical context to identify similarities with previous incidents, understand potential threats, and recommend investigation and containment actions.

---

## 🚨 The Problem

Cybersecurity teams often face challenges such as:

- Repeated investigation of similar security incidents.
- Difficulty recalling lessons from previous incidents.
- Time-consuming manual threat analysis.
- Delays in identifying appropriate containment measures.

Important historical knowledge can be lost between investigations, making incident response slower and less efficient.

## 💡 Our Solution

CyberRecall AI introduces an AI-powered incident response workflow that combines historical memory retrieval and Large Language Models (LLMs).

When a new incident is submitted, the system retrieves relevant historical context and uses AI to generate an actionable analysis.

### ✨ Key Features

- **AI-Powered Threat Analysis:** Analyses submitted cybersecurity incidents.
- **Historical Memory Retrieval:** Uses Hindsight to recall relevant past incident information.
- **Incident Comparison:** Helps identify similarities between current and historical incidents.
- **Risk Assessment:** Generates a risk level for the incident.
- **Investigation Recommendations:** Suggests steps for further investigation.
- **Containment Suggestions:** Provides recommended actions to help limit potential damage.
- **Security Dashboard:** Presents incident information and AI analysis through a user-friendly interface.
- **Incident History:** Helps users review previously submitted incidents.

## ⚙️ How It Works

1. **Incident Submission:** The user submits a cybersecurity incident through the React frontend.
2. **Backend Processing:** FastAPI receives the incident and coordinates the analysis workflow.
3. **Historical Recall:** Hindsight retrieves relevant historical memories.
4. **AI Analysis:** Groq-powered LLM analyses the incident using the historical context.
5. **Actionable Insights:** The system generates a risk level, threat assessment, investigation steps, and containment recommendations.
6. **Results Display:** The frontend presents the generated analysis to the user.

## 🏗️ System Architecture

```text
              USER
                |
                v
        REACT FRONTEND
                |
                v
          FASTAPI BACKEND
                |
          +-----+------+
          |            |
          v            v
       MONGODB      HINDSIGHT
          |        MEMORY RECALL
          |            |
          +-----+------+
                |
                v
           GROQ LLM
                |
                v
        AI INCIDENT ANALYSIS
                |
                v
        RESULTS TO FRONTEND
```

## 🧰 Technology Stack

| Component | Technology |
|---|---|
| Frontend | React.js, Vite |
| Backend | Python, FastAPI |
| AI / LLM | Groq |
| Memory System | Hindsight |
| Database | MongoDB |
| API Testing | Swagger UI |
| Version Control | Git and GitHub |

## 📂 Project Structure

```text
CyberRecall-AI/
│
├── ai-engine/
│
├── backend/
│   ├── config/
│   ├── models/
│   ├── routes/
│   ├── services/
│   └── main.py
│
├── docs/
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

*Note: Folder contents may vary as the project evolves.*

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Node.js and npm
- MongoDB
- Groq API key
- Hindsight configuration

### 1. Clone the Repository

```bash
git clone https://github.com/thejasgowdaar/CyberRecall-AI.git
cd CyberRecall-AI
```

### 2. Set Up the Backend

Create and activate a Python virtual environment if one is not already configured.

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the backend dependencies using the backend requirements file:

```bash
pip install -r backend/requirements.txt
```

Configure the required environment variables in your local `.env` file. Use the variable names expected by the project configuration.

### 3. Set Up the Frontend

```bash
cd frontend
npm install
npm run dev
```

Open the local URL displayed by Vite in your browser.

### 4. Start the Backend

From the project root, start FastAPI using the application's configured entry point.

For example, if the entry point is `backend.main`:

```bash
uvicorn backend.main:app --reload
```

Open the Swagger documentation at:

```text
http://127.0.0.1:8000/docs
```

*Check the actual backend entry point and requirements-file location in the repository before running these commands.*

## 📊 AI Analysis Output

CyberRecall AI is designed to generate:

- **Risk Level:** Low, Medium, High, or Critical.
- **Threat Assessment:** AI-generated explanation of the potential threat.
- **Historical Context:** Relevant information recalled from previous incidents.
- **Recommended Investigation Steps:** Suggested actions for further analysis.
- **Suggested Containment Actions:** Recommended steps to limit the incident's impact.

## 🔐 Security

- Keep API keys and credentials in environment variables.
- Never commit `.env` files or private credentials.
- Do not expose database connection strings or secrets in public repositories.
- Review AI-generated recommendations before taking real-world security actions.

## 🎯 Project Vision

Our vision is to make cybersecurity incident response more intelligent, contextual, and efficient.

By combining historical memory with AI-powered reasoning, CyberRecall AI aims to transform past incident knowledge into actionable intelligence for future investigations.

## 👥 Team

**Built with collaboration, innovation, and a shared vision for smarter cybersecurity.**

Team CyberRecall AI

---

⭐ If you find this project interesting, consider giving the repository a star!

**CyberRecall AI — Remember Every Threat. Respond Smarter.**

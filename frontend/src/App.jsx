
import { useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [incidents, setIncidents] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [showHistory, setShowHistory] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [selectedIncident, setSelectedIncident] = useState(null);

  const [incident, setIncident] = useState({
    title: "",
    description: ""
  });

  const handleSubmit = async (e) => {
    e.preventDefault();

    setLoading(true);
    setError("");

    try {
      const response = await fetch(
        `${API_URL}/api/ai/analyze`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify(incident)
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Analysis failed");
      }

      const newIncident = {
        id: Date.now(),
        title: incident.title,
        description: incident.description,
        date: new Date().toLocaleString(),
        analysis: data.analysis
      };

      setIncidents((prev) => [newIncident, ...prev]);
      setSelectedIncident(newIncident);

      setIncident({
        title: "",
        description: ""
      });

      setShowForm(false);
      setShowHistory(false);

    } catch (err) {
      setError(err.message || "Unable to connect to AI server");
    } finally {
      setLoading(false);
    }
  };

  const severityClass = (severity) => {
    return severity?.toLowerCase() || "medium";
  };

  return (
    <div className="app">

      <header className="navbar">
        <div className="brand">
          <span className="brand-icon">⌘</span>
          CYBERRECALL <span>AI</span>
        </div>

        <div className="nav-status">
          <span className="status-dot"></span>
          AI SECURITY SYSTEM
        </div>
      </header>

      <main className="container">

        <section className="hero">
          <div className="hero-tag">
            INTELLIGENCE · SECURITY · PROTECTION
          </div>

          <h1>
            Cybersecurity, <span>Reimagined.</span>
          </h1>

          <p>
            Detect, analyze and understand cybersecurity
            incidents with AI-powered intelligence.
          </p>
        </section>

        <section className="stats-grid">

          <div className="stat-card">
            <div className="stat-label">TOTAL INCIDENTS</div>
            <div className="stat-number">{incidents.length}</div>
            <div className="stat-note">Reported incidents</div>
          </div>

          <div className="stat-card">
            <div className="stat-label">HIGH RISK</div>
            <div className="stat-number">
              {incidents.filter(
                (item) =>
                  ["High", "Critical"].includes(
                    item.analysis.severity
                  )
              ).length}
            </div>
            <div className="stat-note">High / Critical severity</div>
          </div>

          <div className="stat-card">
            <div className="stat-label">AI ENGINE</div>
            <div className="engine-status">
              <span className="status-dot"></span>
              Groq Connected
            </div>
            <div className="stat-note">Analysis powered by LLM</div>
          </div>

        </section>

        <section className="action-grid">

          <div className="action-card">
            <div className="card-icon blue">01</div>
            <h2>Report Incident</h2>
            <p>
              Submit a suspicious activity or security
              incident for AI analysis.
            </p>
            <button
              className="primary-btn"
              onClick={() => {
                setShowForm(!showForm);
                setShowHistory(false);
                setError("");
              }}
            >
              {showForm ? "Close Form" : "Report Now"}
            </button>
          </div>

          <div className="action-card">
            <div className="card-icon purple">02</div>
            <h2>AI Analysis</h2>
            <p>
              Understand threats, incident classification
              and recommended security actions.
            </p>
            <button
              className="secondary-btn"
              disabled={!selectedIncident}
              onClick={() => {
                setShowForm(false);
                setShowHistory(false);
              }}
            >
              {selectedIncident ? "View Latest Analysis" : "Awaiting Analysis"}
            </button>
          </div>

          <div className="action-card">
            <div className="card-icon green">03</div>
            <h2>Incident History</h2>
            <p>
              Review previously submitted incidents
              and their AI-generated reports.
            </p>
            <button
              className="secondary-btn"
              onClick={() => {
                setShowHistory(!showHistory);
                setShowForm(false);
              }}
            >
              {showHistory ? "Close History" : "View History"}
            </button>
          </div>

        </section>

        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        {showForm && (
          <section className="content-panel">
            <div className="panel-heading">
              <div>
                <span className="eyebrow">NEW SUBMISSION</span>
                <h2>Report a Security Incident</h2>
              </div>
              <span className="panel-number">01 / REPORT</span>
            </div>

            <form onSubmit={handleSubmit} className="incident-form">

              <label>Incident Title</label>
              <input
                type="text"
                placeholder="e.g. Suspicious login activity"
                value={incident.title}
                onChange={(e) =>
                  setIncident({
                    ...incident,
                    title: e.target.value
                  })
                }
                minLength={3}
                maxLength={150}
                required
              />

              <label>Incident Description</label>
              <textarea
                placeholder="Describe what happened, when it happened and any suspicious activity observed..."
                value={incident.description}
                onChange={(e) =>
                  setIncident({
                    ...incident,
                    description: e.target.value
                  })
                }
                minLength={10}
                maxLength={5000}
                required
              />

              <button
                type="submit"
                className="primary-btn submit-btn"
                disabled={loading}
              >
                {loading
                  ? "AI is analyzing..."
                  : "Analyze Incident →"}
              </button>

              {loading && (
                <p className="loading-text">
                  Connecting to Groq AI. Please wait...
                </p>
              )}

            </form>
          </section>
        )}

        {selectedIncident && !showForm && !showHistory && (
          <section className="content-panel">
            <div className="panel-heading">
              <div>
                <span className="eyebrow">GROQ INTELLIGENCE</span>
                <h2>AI Analysis Report</h2>
              </div>
              <span className={`severity ${severityClass(selectedIncident.analysis.severity)}`}>
                {selectedIncident.analysis.severity}
              </span>
            </div>

            <div className="analysis-content">

              <h3>{selectedIncident.title}</h3>

              <div className="analysis-item">
                <span>CLASSIFICATION</span>
                <p>{selectedIncident.analysis.classification}</p>
              </div>

              <div className="analysis-item">
                <span>SUMMARY</span>
                <p>{selectedIncident.analysis.summary}</p>
              </div>

              <div className="analysis-item">
                <span>RISK ASSESSMENT</span>
                <p>{selectedIncident.analysis.risk_level}</p>
              </div>

              <div className="analysis-item">
                <span>RECOMMENDED ACTIONS</span>
                <ul>
                  {selectedIncident.analysis.recommendations.map(
                    (item, index) => (
                      <li key={index}>{item}</li>
                    )
                  )}
                </ul>
              </div>

              <p className="report-date">
                Generated: {selectedIncident.date}
              </p>

            </div>
          </section>
        )}

        {showHistory && (
          <section className="content-panel">
            <div className="panel-heading">
              <div>
                <span className="eyebrow">RECORDS</span>
                <h2>Incident History</h2>
              </div>
            </div>

            {incidents.length === 0 ? (
              <div className="empty-state">
                <h3>No incidents yet</h3>
                <p>Your submitted incidents will appear here.</p>
              </div>
            ) : (
              incidents.map((item) => (
                <div className="history-item" key={item.id}>
                  <div>
                    <h3>{item.title}</h3>
                    <p>{item.date}</p>
                  </div>

                  <span className={`severity ${severityClass(item.analysis.severity)}`}>
                    {item.analysis.severity}
                  </span>

                  <button
                    className="text-btn"
                    onClick={() => {
                      setSelectedIncident(item);
                      setShowHistory(false);
                    }}
                  >
                    View Report →
                  </button>
                </div>
              ))
            )}
          </section>
        )}

        <footer>
          <div className="footer-brand">CYBERRECALL AI</div>
          <p>AI-Powered Cybersecurity Intelligence</p>
          <span>Built with React · FastAPI · Groq</span>
        </footer>

      </main>
    </div>
  );
}

export default App;

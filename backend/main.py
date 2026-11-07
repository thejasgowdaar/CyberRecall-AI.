from fastapi import FastAPI

from backend.routes.incidents import router as incident_router

app = FastAPI(
    title="CyberRecall AI",
    description="AI-Powered Cybersecurity Incident Response System",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to CyberRecall AI API",
        "status": "running"
    }


app.include_router(incident_router)
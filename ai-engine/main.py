
import os
import json
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from groq import Groq


# Load environment variables from ai-engine/.env
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

API_KEY = os.getenv("GROQ_API_KEY")
MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

if not API_KEY:
    raise RuntimeError(
        "GROQ_API_KEY missing. Check ai-engine/.env"
    )

client = Groq(api_key=API_KEY)

app = FastAPI(
    title="CyberRecall AI",
    description="AI-Powered Cybersecurity Intelligence",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Incident(BaseModel):
    title: str = Field(min_length=3, max_length=150)
    description: str = Field(min_length=10, max_length=5000)


@app.get("/")
def home():
    return {
        "success": True,
        "message": "CyberRecall AI Backend Running"
    }


@app.get("/api/health")
def health():
    return {
        "success": True,
        "message": "AI backend is ready"
    }


@app.post("/api/ai/analyze")
def analyze_incident(incident: Incident):

    try:
        response = client.chat.completions.create(
            model=MODEL,

            messages=[
                {
                    "role": "system",
                    "content": """
You are CyberRecall AI, an expert cybersecurity
incident analysis assistant.

Analyze the incident carefully.

Return ONLY valid JSON with these fields:

{
  "classification": "Type of cybersecurity incident",
  "severity": "Low, Medium, High or Critical",
  "summary": "Clear explanation of the incident",
  "risk_level": "Short risk assessment",
  "recommendations": [
    "First recommended action",
    "Second recommended action",
    "Third recommended action"
  ]
}

Rules:
1. Never claim an attack is confirmed without evidence.
2. Do not invent technical evidence.
3. Explain the potential security risks.
4. Give practical recommendations.
5. Severity must be Low, Medium, High or Critical.
6. Return recommendations as a JSON list.
"""
                },
                {
                    "role": "user",
                    "content": (
                        f"Incident title: {incident.title}\n"
                        f"Incident description: {incident.description}"
                    )
                }
            ],

            response_format={"type": "json_object"},
            temperature=0.2,
            max_completion_tokens=1000
        )

        content = response.choices[0].message.content

        if not content:
            raise ValueError("Empty AI response")

        result = json.loads(content)

        required_fields = [
            "classification",
            "severity",
            "summary",
            "risk_level",
            "recommendations"
        ]

        for field in required_fields:
            if field not in result:
                raise ValueError(f"Missing field: {field}")

        if result["severity"] not in [
            "Low", "Medium", "High", "Critical"
        ]:
            result["severity"] = "Medium"

        if not isinstance(result["recommendations"], list):
            raise ValueError("Invalid recommendations format")

        return {
            "success": True,
            "analysis": result
        }

    except Exception as error:
        print("AI analysis error:", str(error))

        raise HTTPException(
            status_code=500,
            detail="AI analysis failed. Check backend terminal."
        )

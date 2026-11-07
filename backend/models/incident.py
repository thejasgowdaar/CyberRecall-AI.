from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, timezone


class Incident(BaseModel):

    incident_id: Optional[str] = None

    title: str = Field(..., min_length=3)

    category: str

    description: str

    indicators: List[str] = []

    findings: List[str] = []

    resolution: Optional[str] = None

    status: str = "new"

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
class IncidentVerification(BaseModel):
    findings: List[str] = Field(default_factory=list)
    resolution: str = Field(..., min_length=5)
    analyst_verified: bool = False    
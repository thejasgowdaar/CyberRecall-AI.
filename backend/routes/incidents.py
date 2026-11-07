from backend.models.incident import IncidentVerification
from backend.services.memory_service import MemoryService
from starlette.concurrency import run_in_threadpool
from backend.services.groq_service import analyze_incident
from fastapi import APIRouter, HTTPException
from bson import ObjectId

from backend.config.database import db
from backend.models.incident import Incident
from backend.services.comparison_service import IncidentComparison

router = APIRouter(
    prefix="/incidents",
    tags=["Incidents"]
)

incident_collection = db["incidents"]


# 1. Submit a new incident
@router.post("/")
def create_incident(incident: Incident):

    try:
        incident_data = incident.model_dump(
            exclude={"incident_id"}
        )

        result = incident_collection.insert_one(
            incident_data
        )

        response_data = incident.model_dump(
            mode="json",
            exclude={"incident_id"}
        )

        return {
            "message": "Incident submitted successfully",
            "incident_id": str(result.inserted_id),
            "incident": response_data
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# 2. Retrieve all incidents
@router.get("/")
def get_incidents():

    try:
        incidents = list(
            incident_collection.find().sort(
                "created_at", -1
            )
        )

        for incident in incidents:
            incident["incident_id"] = str(
                incident.pop("_id")
            )

        return {
            "total": len(incidents),
            "incidents": incidents
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# 3. Retrieve one incident by ID
@router.get("/{incident_id}")
def get_incident(incident_id: str):

    try:
        if not ObjectId.is_valid(incident_id):
            raise HTTPException(
                status_code=400,
                detail="Invalid incident ID"
            )

        incident = incident_collection.find_one({
            "_id": ObjectId(incident_id)
        })

        if not incident:
            raise HTTPException(
                status_code=404,
                detail="Incident not found"
            )

        incident["incident_id"] = str(
            incident.pop("_id")
        )

        return incident

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# 4. Compare incident with Hindsight history
@router.post("/{incident_id}/compare")
def compare_incident_with_history(incident_id: str):

    try:
        if not ObjectId.is_valid(incident_id):
            raise HTTPException(
                status_code=400,
                detail="Invalid incident ID"
            )

        incident = incident_collection.find_one({
            "_id": ObjectId(incident_id)
        })

        if not incident:
            raise HTTPException(
                status_code=404,
                detail="Incident not found"
            )

        incident["incident_id"] = str(
            incident.pop("_id")
        )

        comparison = IncidentComparison()

        try:
            return comparison.compare_with_history(incident)
        finally:
            comparison.close()

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )
        
# 5. Analyze incident using Hindsight + Groq
@router.post("/{incident_id}/analyze")
async def analyze_incident_with_ai(incident_id: str):
    comparison = None

    try:
        if not ObjectId.is_valid(incident_id):
            raise HTTPException(
                status_code=400,
                detail="Invalid incident ID"
            )

        incident = incident_collection.find_one(
            {"_id": ObjectId(incident_id)}
        )

        if not incident:
            raise HTTPException(
                status_code=404,
                detail="Incident not found"
            )

        incident["incident_id"] = str(incident.pop("_id"))

        comparison = IncidentComparison()

        # Run synchronous Hindsight operations in a worker thread
        comparison_result = await run_in_threadpool(
            comparison.compare_with_history,
            incident
        )

        historical_memories = comparison_result["historical_memories"]

        # Groq is asynchronous, so await it normally
        ai_analysis = await analyze_incident(
            incident,
            historical_memories
        )

        return {
            "incident_id": incident_id,
            "total_matches": len(historical_memories),
            "historical_memories": historical_memories,
            "ai_analysis": ai_analysis
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

    finally:
        if comparison is not None:
            await run_in_threadpool(comparison.close)
@router.post("/{incident_id}/verify")
def verify_incident(
    incident_id: str,
    verification: IncidentVerification
):
    memory = None

    try:
        if not ObjectId.is_valid(incident_id):
            raise HTTPException(
                status_code=400,
                detail="Invalid incident ID"
            )

        if not verification.analyst_verified:
            raise HTTPException(
                status_code=400,
                detail="Analyst verification is required"
            )

        incident = incident_collection.find_one(
            {"_id": ObjectId(incident_id)}
        )

        if not incident:
            raise HTTPException(
                status_code=404,
                detail="Incident not found"
            )

        if incident.get("status") == "verified":
            raise HTTPException(
                status_code=409,
                detail="Incident is already verified"
            )

        incident_collection.update_one(
            {"_id": ObjectId(incident_id)},
            {
                "$set": {
                    "findings": verification.findings,
                    "resolution": verification.resolution,
                    "status": "verified_pending_memory"
                }
            }
        )

        memory_content = {
            "incident_id": incident_id,
            "title": incident.get("title"),
            "category": incident.get("category"),
            "description": incident.get("description"),
            "indicators": incident.get("indicators", []),
            "verified_findings": verification.findings,
            "confirmed_resolution": verification.resolution,
            "analyst_verified": True
        }

        memory = MemoryService()
        memory.save_memory(memory_content)

        incident_collection.update_one(
            {"_id": ObjectId(incident_id)},
            {"$set": {"status": "verified"}}
        )

        return {
            "message": "Incident verified and saved to Hindsight",
            "incident_id": incident_id,
            "status": "verified"
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

    finally:
        if memory is not None:
            memory.close()            
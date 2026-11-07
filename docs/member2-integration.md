# CyberRecall AI - Member 2 Integration

## Module
Hindsight Memory Integration

## Memory Bank
cyberrecall-team

## Main Service
backend/services/memory_service.py

## Functions

### 1. Save Memory
Function: save_memory(incident)

Purpose:
Stores cybersecurity incident knowledge in Hindsight.

Input:
Incident details as a string or dictionary.

### 2. Search Memory
Function: search_memory(query)

Purpose:
Retrieves relevant historical memories.

Input:
A natural-language search query.

### 3. Close Connection
Function: close()

Purpose:
Closes the Hindsight client.

## Other Services
- memory_insights.py
- comparison_service.py

## Responsibilities
- Store incident investigation knowledge.
- Retrieve historical incidents.
- Provide historical context to AI analysis.
- Supply memory information for dashboard insights.

## Important
Retrieved memories are historical context.
They must not automatically be treated as proof
that two incidents have the same attacker.
## Team Integration Instructions

### Member 1 – FastAPI Backend

After an analyst confirms an incident's findings and resolution,
save the incident:

from backend.services.memory_service import MemoryService

memory = MemoryService()
memory.save_memory(incident)

### Member 3 – AI Analysis

Before generating recommendations, retrieve historical context:

from backend.services.memory_service import MemoryService

memory = MemoryService()
history = memory.search_memory(
    "Previous incidents related to this incident"
)

Pass the retrieved history to the Groq analysis module.

### Member 4 – Frontend

Display historical incidents and AI recommendations
using the API responses provided by Member 1.
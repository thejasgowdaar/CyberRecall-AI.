from backend.services.memory_service import MemoryService


class IncidentComparison:

    def __init__(self):
        self.memory = MemoryService()

    def compare_with_history(self, incident):

        query = f"""
        Find previous cybersecurity incidents similar to this new incident.

        Incident title: {incident.get('title', '')}
        Category: {incident.get('category', '')}
        Description: {incident.get('description', '')}
        Indicators: {', '.join(incident.get('indicators', []))}

        Retrieve previous investigations, indicators,
        findings and confirmed resolutions.
        """

        result = self.memory.search_memory(query)

        historical_memories = []

        for item in result.results:

            historical_memories.append({
                "memory_id": item.id,
                "type": item.type,
                "description": item.text
            })

        return {
            "new_incident": incident,
            "historical_memories": historical_memories,
            "total_matches": len(historical_memories)
        }

    def close(self):
        self.memory.client.close()
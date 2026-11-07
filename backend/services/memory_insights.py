from backend.services.memory_service import MemoryService


class MemoryInsights:

    def __init__(self):
        self.memory = MemoryService()

    def get_insights(self, query):

        result = self.memory.search_memory(query)

        insights = []

        for item in result.results:

            insights.append({
                "memory_id": item.id,
                "memory_type": item.type,
                "description": item.text
            })

        return {
            "total_memories": len(insights),
            "memories": insights
        }

    def close(self):
        self.memory.client.close()
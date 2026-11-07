import json

from hindsight_client import Hindsight

from backend.config.hindsight_config import (
    HINDSIGHT_API_URL,
    HINDSIGHT_API_KEY,
    HINDSIGHT_BANK_ID
)


class MemoryService:

    def __init__(self):

        if not HINDSIGHT_API_KEY:
            raise ValueError("Hindsight API key is missing.")

        self.client = Hindsight(
            base_url=HINDSIGHT_API_URL,
            api_key=HINDSIGHT_API_KEY
        )

        self.bank_id = HINDSIGHT_BANK_ID

    # Save incident knowledge into Hindsight
    def save_memory(self, incident):

        if isinstance(incident, dict):
            incident = json.dumps(incident, indent=2)

        return self.client.retain(
            bank_id=self.bank_id,
            content=incident
        )

    # Retrieve relevant historical knowledge
    def search_memory(self, query):

        return self.client.recall(
            bank_id=self.bank_id,
            query=query
        )

    # Close Hindsight client
    def close(self):

        self.client.close()
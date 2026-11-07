from backend.services.memory_service import MemoryService


def main():

    memory = MemoryService()

    try:
        print("\nSearching previous incidents...")

        result = memory.search_memory(
            "Previous Microsoft phishing incidents"
        )

        print("\nRetrieved memories:")
        print(result)

    finally:
        memory.client.close()


if __name__ == "__main__":
    main()
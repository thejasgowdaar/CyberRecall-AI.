from backend.services.memory_insights import MemoryInsights


def main():

    insights_service = MemoryInsights()

    try:

        result = insights_service.get_insights(
            "Previous cybersecurity phishing incidents "
            "and their investigation resolutions"
        )

        print("\n========== CYBERRECALL MEMORY INSIGHTS ==========")

        print("Total memories:", result["total_memories"])

        for memory in result["memories"]:

            print("\nMemory ID:", memory["memory_id"])
            print("Type:", memory["memory_type"])
            print("Description:", memory["description"])

        print("\n================================================")

    finally:
        insights_service.close()


if __name__ == "__main__":
    main()
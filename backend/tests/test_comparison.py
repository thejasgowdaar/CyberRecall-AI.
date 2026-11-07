from backend.services.comparison_service import IncidentComparison


def main():

    comparison = IncidentComparison()

    new_incident = {
        "title": "Suspicious Microsoft login email",
        "category": "Phishing",
        "description": (
            "An employee received an email pretending "
            "to be from Microsoft, containing a suspicious login link."
        ),
        "indicators": [
            "Suspicious sender",
            "Fake login page",
            "Microsoft impersonation"
        ]
    }

    try:

        print("\n========== INCIDENT COMPARISON ==========")

        result = comparison.compare_with_history(new_incident)

        print("\nNew incident:")
        print(result["new_incident"]["title"])

        print("\nHistorical memories found:")
        print(result["total_matches"])

        for memory in result["historical_memories"]:

            print("\nMemory ID:", memory["memory_id"])
            print("Type:", memory["type"])
            print("Description:", memory["description"])

        print("\n=========================================")

    finally:
        comparison.close()


if __name__ == "__main__":
    main()
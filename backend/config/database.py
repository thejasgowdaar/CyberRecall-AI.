import os
from pymongo import MongoClient
from dotenv import load_dotenv

from pathlib import Path

# Load environment variables from project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")

# MongoDB configuration
MONGODB_URI = os.getenv(
    "MONGODB_URI",
    "mongodb://127.0.0.1:27017/"
)

DATABASE_NAME = os.getenv(
    "DATABASE_NAME",
    "cyberrecall_ai"
)

# Connect to MongoDB
client = MongoClient(
    MONGODB_URI,
    serverSelectionTimeoutMS=5000
)

# Select database
db = client[DATABASE_NAME]


def test_connection():
    try:
        client.admin.command("ping")
        print("MongoDB connected successfully!")
        return True

    except Exception as error:
        print("MongoDB connection failed:", error)
        return False
import os
from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]

load_dotenv(PROJECT_ROOT / ".env")

HINDSIGHT_API_URL = "https://api.hindsight.vectorize.io"

HINDSIGHT_API_KEY = os.getenv("HINDSIGHT_API_KEY")

HINDSIGHT_BANK_ID = os.getenv("HINDSIGHT_BANK_ID")
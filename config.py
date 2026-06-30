import os
from pathlib import Path
from dotenv import load_dotenv
import logging

load_dotenv()

# --- API Configuration ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable is not set")

# --- Application Configuration ---
PROJECT_NAME = "Career Market Engine"
DB_PATH = os.getenv("DB_PATH", "career_market.db")
GITHUB_URL = "https://raw.githubusercontent.com/SimplifyJobs/New-Grad-Positions/dev/README.md"

# --- Feature Flags ---
DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"
SENTRY_DSN = os.getenv("SENTRY_DSN", "")

# --- Logging Configuration ---
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "logs/app.log")

# Create logs directory if it doesn't exist
log_dir = Path(LOG_FILE).parent
log_dir.mkdir(parents=True, exist_ok=True)

# --- Environment Documentation ---
"""
Required Environment Variables:
- GROQ_API_KEY: Your Groq API key (get from https://console.groq.com)
- DB_PATH: (optional) Path to SQLite database (default: career_market.db)
- DEBUG_MODE: (optional) Enable debug logging (default: false)
- SENTRY_DSN: (optional) Sentry error tracking URL
- LOG_LEVEL: (optional) Logging level (default: INFO)
- LOG_FILE: (optional) Log file path (default: logs/app.log)

Example .env file:
    GROQ_API_KEY=gsk_xxxxxxxxxxxx
    DEBUG_MODE=false
    LOG_LEVEL=INFO
"""

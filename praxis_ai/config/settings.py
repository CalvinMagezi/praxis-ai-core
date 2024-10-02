# config/settings.py

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Praxis AI Configuration
PRAXIS_NAME = "Praxis AI"
PRAXIS_VERSION = "1.0.0"

# Ell Configuration
ELL_STORE_PATH = './ell_logdir'
ELL_AUTOCOMMIT = True

# Model Configuration
ORCHESTRATOR_MODEL = "gpt-4o"
SUB_AGENT_MODEL = "gpt-4o-mini"
REFINER_MODEL = "gpt-4o-mini"
CHAT_MODEL = "gpt-4o-mini"

# Logging Configuration
LOG_LEVEL = "INFO"
LOG_FILE = "praxis_ai.log"

# API Configuration (for future use)
API_HOST = "0.0.0.0"
API_PORT = 8000

# API Key Configuration
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  

# Google Calendar API settings
GOOGLE_CALENDAR_CREDENTIALS_FILE =  os.getenv("GOOGLE_CALENDAR_CREDENTIALS_FILE")

missing_keys = []
if not TAVILY_API_KEY:
    missing_keys.append("TAVILY_API_KEY")
if not OPENAI_API_KEY:
    missing_keys.append("OPENAI_API_KEY")
if not GOOGLE_CALENDAR_CREDENTIALS_FILE:
    missing_keys.append("GOOGLE_CALENDAR_CREDENTIALS_FILE")

if missing_keys:
    raise ValueError(f"The following API key(s) are not set in the environment variables or .env file: {', '.join(missing_keys)}")
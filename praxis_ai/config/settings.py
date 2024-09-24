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
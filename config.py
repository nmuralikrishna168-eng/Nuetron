import os

# Gemini API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")

# Ollama Configuration
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "llama3.2"  # or mistral, phi3

# User Configuration
USER_NAME = "Murali Krishna"

# Application Configuration
APP_TITLE = "NUETRON v16 - Think • Create • Automate"
APP_MIN_WIDTH = 1200
APP_MIN_HEIGHT = 780

# Audio Configuration
SPEECH_RATE = 175
PAUSE_THRESHOLD = 0.8
LISTEN_TIMEOUT = 5

# Generated Projects Directory
GENERATED_PROJECTS_DIR = "generated_projects"

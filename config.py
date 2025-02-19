import os
from dotenv import load_dotenv

# Load API Keys from .env file
load_dotenv()

SAM_GOV_API_KEY = os.getenv("SAM_GOV_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Check if the API keys are loaded
if not SAM_GOV_API_KEY:
    raise ValueError("SAM.gov API Key not found. Make sure it's in the .env file.")
if not OPENAI_API_KEY:
    raise ValueError("OpenAI API Key not found. Make sure it's in the .env file.")
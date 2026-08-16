import os
from pathlib import Path

from dotenv import load_dotenv

# get the parent directory of the current file
PROJECT_ROOT = Path(__file__).resolve().parents[1]
# get the path to the .env file
ENV_PATH = PROJECT_ROOT/".env"

# load the VirusTotal API key from the environment
def load_api_key() -> str:

    load_dotenv(ENV_PATH)

    api_key = os.getenv("VT_API_KEY")

    if not api_key:
        raise ValueError(
            "VT_API_KEY is not set."
        )

    return api_key
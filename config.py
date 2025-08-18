
import os
from dotenv import load_dotenv

# Load environment variables from a .env file if it exists
load_dotenv()

# --- Configuration ---
BELT_CAPACITY = int(os.environ.get("BELT_CAPACITY", 10))
NUM_PRODUCERS = int(os.environ.get("NUM_PRODUCERS", 2))
NUM_CONSUMERS = int(os.environ.get("NUM_CONSUMERS", 3))
SIMULATION_DURATION_SECONDS = int(os.environ.get("SIMULATION_DURATION_SECONDS", 15))

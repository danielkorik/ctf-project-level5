from dotenv import load_dotenv
import os
import validators
from logger import logger, setup_logger  # Import logger and setup_logger from logger.py

# Load environment variables from the .env.devs.dev file
load_dotenv()

# Fetch environment variables
ENV = os.getenv('ENV', 'dev').lower()  # Default to 'dev' if not set
BASE_URL = os.getenv('BASE_URL')
PORT = os.getenv('PORT', '80')  # Default to port 80 if not set
ENDPOINT_PATH = os.getenv('ENDPOINT_PATH')

# Construct the full endpoint URL
ENDPOINT_URL = f"{BASE_URL}:{PORT}{ENDPOINT_PATH}"

# Configure the logger based on the environment
setup_logger(ENV)

# Validate ENV variable
if ENV not in ['dev', 'release']:
    logger.warning("Invalid ENV value, defaulting to 'dev'")
    ENV = 'dev'

# Validate the constructed ENDPOINT_URL
if not BASE_URL or not validators.url(ENDPOINT_URL):
    raise ValueError("Invalid or missing ENDPOINT_URL components")

logger.info(f"Environment: {ENV}, Endpoint URL: {ENDPOINT_URL}")

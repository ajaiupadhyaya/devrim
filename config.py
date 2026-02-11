"""Configuration settings for LinkedIn automation tool."""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# LinkedIn credentials
LINKEDIN_EMAIL = os.getenv('LINKEDIN_EMAIL', '')
LINKEDIN_PASSWORD = os.getenv('LINKEDIN_PASSWORD', '')

# Connection settings
MAX_CONNECTIONS_PER_SESSION = int(os.getenv('MAX_CONNECTIONS_PER_SESSION', '20'))
DELAY_BETWEEN_CONNECTIONS = int(os.getenv('DELAY_BETWEEN_CONNECTIONS', '5'))

# Message template
DEFAULT_MESSAGE_TEMPLATE = os.getenv(
    'MESSAGE_TEMPLATE',
    "Hi {name}, I noticed you work at {company} as a {role}. "
    "I'm interested in the {sector} sector and would love to connect!"
)

# Browser settings
HEADLESS_MODE = os.getenv('HEADLESS_MODE', 'False').lower() == 'true'

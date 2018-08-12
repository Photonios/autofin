import os

from os import environ
from dotenv import load_dotenv, find_dotenv

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Load env vars from a file if it exists
dot_file = os.path.join(root_dir, "local.env")
load_dotenv(dotenv_path=dot_file)

# Twillio configuration
TWILLIO_ACCOUNT_SID = environ.get("TWILLIO_ACCOUNT_SID", None)
TWILLIO_AUTH_TOKEN = environ.get("TWILLIO_AUTH_TOKEN", None)
TWILLIO_PHONE_NUMBER = environ.get("TWILLIO_PHONE_NUMBER", None)
TWILLIO_WEBHOOK_SERVER_PORT = int(environ.get("TWILLIO_WEBHOOK_SERVER_PORT", "32500"))

# Message configuration
MESSAGE_HEADER = "Autofin"

# Creditor configuration
CREDITORS = {
    "eon": environ.get("EON_CREDENTIALS", "").split(":"),
    "upc": environ.get("UPC_CREDENTIALS", "").split(":"),
    "digi": environ.get("DIGI_CREDENTIALS", "").split(":"),
    "electrica": environ.get("ELECTRICA_CREDENTIALS", "").split(":"),
}

# Storage configuration
STORAGE_PATH = environ.get("STORAGE_PATH", os.path.join(root_dir, "db"))

# Sentry configuration
SENTRY_DSN = environ.get("SENTRY_DSN", None)
SENTRY_ENVIRONMENT = environ.get("SENTRY_ENVIRONMENT", "live")

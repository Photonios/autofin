from os import environ


# Twillio configuration
TWILLIO_ACCOUNT_SID = environ.get(
    "TWILLIO_ACCOUNT_SID", "AC5d751b71f3e7e5a980ccd386286fc2c7"
)
TWILLIO_AUTH_TOKEN = environ.get(
    "TWILLIO_AUTH_TOKEN", "26290cba2e5e882cf8cdf9397d514f0d"
)
TWILLIO_PHONE_NUMBER = environ.get("TWILLIO_PHONE_NUMBER", "+3197014200803")
TWILLIO_WEBHOOK_SERVER_PORT = int(environ.get("TWILLIO_WEBHOOK_SERVER_PORT", "32500"))

# Message configuration
MESSAGE_HEADER = "Autofin"

# Creditor configuration
CREDITORS = {
    "electrica": environ.get(
        "ELECTRICA_CREDENTIALS", "adela.suhani@gmail.com:aoeuid123"
    ).split(":")
}

# Storage configuration
STORAGE_PATH = environ.get("STORAGE_PATH", "/Users/swen/Code/autofin/db")

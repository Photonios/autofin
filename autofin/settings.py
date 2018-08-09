from os import environ


# Twillio configuration
TWILLIO_ACCOUNT_SID = environ.get(
    "TWILLIO_ACCOUNT_SID", "AC5d751b71f3e7e5a980ccd386286fc2c7"
)
TWILLIO_AUTH_TOKEN = environ.get(
    "TWILLIO_AUTH_TOKEN", "26290cba2e5e882cf8cdf9397d514f0d"
)
TWILLIO_SERVICE_ID = environ.get(
    "TWILLIO_SERVICE_ID", "MG6c4c1791a0024364bfbc58d67f1c27a2"
)
TWILLIO_SENDER_NAME = environ.get("TWILLIO_SENDER_NAME", "Autofin")

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

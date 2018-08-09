import structlog

from twilio.rest import Client

from autofin import User, settings, storage

LOGGER = structlog.get_logger(__name__)


def notify_one(user: User, message: str) -> None:
    """Notify the specified user with the specified message."""

    twillio_client = Client(settings.TWILLIO_ACCOUNT_SID, settings.TWILLIO_AUTH_TOKEN)

    twillio_client.messages.create(
        messaging_service_sid="MG6c4c1791a0024364bfbc58d67f1c27a2",
        body=message,
        to=user.phone_number,
    )

    LOGGER.info("Send notification to", user=user, message=message)


def notify_all(message: str) -> None:
    """Notifies all registered users with the specified message."""

    for user in storage.users:
        notify_one(user, message)

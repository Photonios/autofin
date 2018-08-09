import structlog

from twilio.rest import Client

from autofin import User, settings, storage

LOGGER = structlog.get_logger(__name__)


def notify_one(user: User, message: str) -> None:
    """Notify the specified user with the specified message."""

    twillio_client = Client(settings.TWILLIO_ACCOUNT_SID, settings.TWILLIO_AUTH_TOKEN)

    twillio_client.messages.create(
        from_=settings.TWILLIO_PHONE_NUMBER, body=message, to=user.phone_number
    )

    LOGGER.info("Send notification to", user=user, message=message)


def notify_all(message: str) -> None:
    """Notifies all registered users with the specified message."""

    for user in storage.users:
        notify_one(user, message)

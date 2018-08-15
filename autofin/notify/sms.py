import structlog

from twilio.rest import Client

from autofin import settings, models
from autofin.contact import ContactMethod

LOGGER = structlog.get_logger(__name__)


def sms(user: models.User, message: str) -> None:
    """Notify the specified user with the specified message."""

    twillio_client = Client(settings.TWILLIO_ACCOUNT_SID, settings.TWILLIO_AUTH_TOKEN)

    for phone_number in user.enabled_phone_numbers:
        twillio_client.messages.create(
            from_=settings.TWILLIO_PHONE_NUMBER, body=message, to=phone_number
        )

        LOGGER.info("Send SMS to", user=user, message=message)

import structlog

from twilio.rest import Client

from autofin import settings, storage
from autofin.billing import InvoiceManager

LOGGER = structlog.get_logger(__name__)


def send_invoices():
    invoices = "\n".join(
        [str(invoice) for invoice in InvoiceManager().get_latest_invoices()]
    )

    message = "%s - Bills overview\n\n%s" % (settings.MESSAGE_HEADER, invoices)

    twillio_client = Client(settings.TWILLIO_ACCOUNT_SID, settings.TWILLIO_AUTH_TOKEN)

    for user in storage.users:
        twillio_client.messages.create(
            messaging_service_sid="MG6c4c1791a0024364bfbc58d67f1c27a2",
            body=message,
            to=user.phone_number,
        )

        LOGGER.info("Send bills overview to", user=user)


if __name__ == "__main__":
    send_invoices()

import structlog

from twilio.rest import Client

from autofin.billing import InvoiceManager
from autofin.messaging import MessageFormatter, notify_all

LOGGER = structlog.get_logger(__name__)


def send_invoices():
    """Sends an overview of the latest invoices to all
    registered users."""

    invoices = InvoiceManager().get_latest_invoices()
    message = MessageFormatter.invoices(invoices)

    notify_all(message)


if __name__ == "__main__":
    send_invoices()

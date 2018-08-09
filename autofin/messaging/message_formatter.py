from typing import List

from autofin import settings
from autofin.billing import Invoice


class MessageFormatter:
    """Assists in formatting notification messages."""

    @staticmethod
    def invoices(invoices: List[Invoice]) -> str:
        """Formats a message with a list of invoices."""
        invoices = "\n".join([str(invoice) for invoice in invoices])

        message = "%s - Bills overview\n\n%s" % (settings.MESSAGE_HEADER, invoices)
        return message

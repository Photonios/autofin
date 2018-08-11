from typing import List

from autofin import settings
from autofin.billing import Invoice


class MessageFormatter:
    """Assists in formatting notification messages."""

    @staticmethod
    def invoices(invoices: List[Invoice]) -> str:
        """Formats a message with a list of invoices."""
        invoices = "\n\n".join([str(invoice) for invoice in invoices])

        message = "%s - Bills overview\n\n%s" % (settings.MESSAGE_HEADER, invoices)
        return message

    @staticmethod
    def unknown_command(command: str) -> str:
        """Formats the message for an unknown command."""

        message = "%s - Unknown command\n\n" % settings.MESSAGE_HEADER
        message += "'%s' is not a known command. Did you spell it correctly?" % command

        return message

    @staticmethod
    def error(error_id: str) -> str:
        """Formats a message for an error that occurred."""

        message = "%s - Something went wrong\n\n" % settings.MESSAGE_HEADER
        message += "Error ID: %s" % error_id
        message += "\n\nPlease try again."

        return message

from datetime import datetime

from .payment_status import PaymentStatus


class Invoice:
    """Represents a bill/invoice of a company."""

    def __init__(
        self,
        creditor: str,
        amount: float,
        date: datetime,
        due_date: datetime,
        payment_status: PaymentStatus,
    ):
        """Initializes a new instance of :see:Bill.

        Arguments:
            creditor:
                Name of the person/entity that is invoicing.

            amount:
                The total amount payable (in money).

            date:
                The date the bill came in.

            due_date:
                The date the bill should be paid.

            payment_status:
                Whether the bill was paid.
        """

        self.creditor = creditor
        self.amount = amount
        self.date = date
        self.due_date = due_date
        self.payment_status = payment_status

    def __str__(self):
        """Gets a human-readable textual representation of this invoice."""

        payment_status_map = {
            PaymentStatus.UNPAID: "unpaid",
            PaymentStatus.PAID_UNCONFIRMED: "paid, unconfirmed",
            PaymentStatus.PAID_CONFIRMED: "paid, confirmed",
        }

        textual = "%s" % self.creditor
        textual += "\nDate: %s" % self.date.strftime("%d-%b-%Y")
        textual += "\nDue on: %s" % self.due_date.strftime("%d-%b-%Y")
        textual += "\nAmount: %s RON" % self.amount
        textual += (
            "\nStatus: %s" % payment_status_map.get(self.payment_status) or "unknown"
        )

        return textual

    def __repr__(self):
        """Gets a textual representation of this invoice."""
        return str(
            [self.creditor, self.amount, self.date, self.due_date, self.payment_status]
        )

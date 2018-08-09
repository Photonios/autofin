from autofin.util import GlorifiedEnum


class PaymentStatus(GlorifiedEnum):
    """Statuses a payment can be in."""

    UNPAID = "unpaid"
    PAID_UNCONFIRMD = "paid_unconfirmed"
    PAID_CONFIRMED = "paid_confirmed"

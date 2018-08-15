from autofin.util import GlorifiedEnum


class PaymentStatus(GlorifiedEnum):
    """Statuses a payment can be in."""

    UNPAID = 0
    PAID_UNCONFIRMED = 1
    PAID_CONFIRMED = 2

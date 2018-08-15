from peewee import DateField, FloatField, ForeignKeyField

from autofin.billing import Currency, PaymentStatus

from .model import Model
from .user import User
from .creditor import Creditor
from .enum_field import IntegerEnumField


class Invoice(Model):
    """An invoice from a creditor for a user."""

    user = ForeignKeyField(User, backref="invoices")
    creditor = ForeignKeyField(Creditor, backref="invoices")

    amount = FloatField()
    currency = IntegerEnumField(Currency, default=Currency.EUR)
    invoiced_on = DateField()
    due_on = DateField()
    paid_on = DateField(null=True, default=None)
    payment_status = IntegerEnumField(PaymentStatus, default=PaymentStatus.UNPAID)

    class Meta:
        indexes = ((("user", "creditor", "invoiced_on", "due_on"), True),)

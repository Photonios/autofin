from peewee import CharField

from autofin.billing.creditors import CreditorID

from .model import Model
from .enum_field import IntegerEnumField


class Creditor(Model):
    """Single creditor."""

    id = IntegerEnumField(primary_key=True, unique=True, enum=CreditorID)
    name = CharField(max_length=255)

from peewee import BooleanField, CharField, ForeignKeyField

from .model import Model
from .user import User
from .creditor import Creditor


class UserCreditorConfig(Model):
    """Configuration for a creditor, linked to a user."""

    user = ForeignKeyField(User, backref="creditors")
    creditor = ForeignKeyField(Creditor, backref="configs")

    username = CharField(max_length=255)
    password = CharField(max_length=255)

    enabled = BooleanField(default=True)

    class Meta:
        indexes = ((("user", "creditor"), True),)

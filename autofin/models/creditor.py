from peewee import CharField, ForeignKeyField

from .model import Model
from .user import User


class Creditor(Model):
    """A creditor that the user has configured."""

    user = ForeignKeyField(User, backref="creditors")

    name = CharField(max_length=255)
    username = CharField(max_length=255)
    password = CharField(max_length=255)

from peewee import CharField, ForeignKeyField

from .model import Model
from .user import User


class PhoneNumber(Model):
    """A phone number belonging to a user."""

    user = ForeignKeyField(User, backref="phone_numbers")
    value = CharField(max_length=100)

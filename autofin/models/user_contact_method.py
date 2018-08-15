from peewee import BooleanField, CharField, ForeignKeyField

from autofin.contact import ContactMethod

from .model import Model
from .user import User
from .enum_field import IntegerEnumField


class UserContactMethod(Model):
    """A method of contact for a user."""

    user = ForeignKeyField(User, backref="contact_methods")
    method = IntegerEnumField(enum=ContactMethod)
    value = CharField(max_length=255, unique=True)
    enabled = BooleanField(default=True)

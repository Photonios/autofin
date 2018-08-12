from peewee import CharField

from .model import Model


class User(Model):
    """A single user in Autofin."""

    first_name = CharField(max_length=255)
    middle_name = CharField(max_length=255, null=True)
    last_name = CharField(max_length=255)

    email = CharField(max_length=255)
    password = CharField(max_length=128)

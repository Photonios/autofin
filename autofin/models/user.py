from peewee import CharField
from typing import Optional

from autofin.contact import ContactMethod

from .model import Model


class User(Model):
    """A single user in Autofin."""

    first_name = CharField(max_length=255)
    middle_name = CharField(max_length=255, null=True)
    last_name = CharField(max_length=255)

    email = CharField(max_length=255)
    password = CharField(max_length=128)

    @property
    def enabled_phone_numbers(self):
        """Gets the user's enabled phone numbers."""

        from .user_contact_method import UserContactMethod

        contact_methods = self.contact_methods.select().where(
            (UserContactMethod.method == ContactMethod.PHONE)
            & (UserContactMethod.enabled == True)
        )

        return [contact_method.value for contact_method in contact_methods]

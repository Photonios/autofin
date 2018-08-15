import argparse
import structlog

from typing import Optional

from autofin import models, crypto
from autofin.contact import ContactMethod

LOGGER = structlog.get_logger(__name__)


def create(
    first_name: str,
    middle_name: Optional[str],
    last_name: str,
    email: str,
    password: str,
    phone_number: Optional[str],
) -> models.User:
    """Creates a new user."""

    password = crypto.hash_password(email, password)

    user = models.User.create(
        first_name=first_name,
        middle_name=middle_name or None,
        last_name=last_name,
        email=email,
        password=password,
    )

    models.UserContactMethod.create(user=user, method=ContactMethod.EMAIL, value=email)
    if phone_number:
        models.UserContactMethod.create(
            user=user, method=ContactMethod.PHONE, value=phone_number
        )

    LOGGER.info(
        "Created new user",
        id=user.id,
        first_name=first_name,
        middle_name=middle_name or None,
        last_name=last_name,
        email=email,
        password=password,
        phone_number=phone_number,
    )

    return user

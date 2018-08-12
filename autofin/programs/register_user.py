import argparse
import structlog

from typing import Optional

from autofin import models, crypto

LOGGER = structlog.get_logger(__name__)


def register_user(
    first_name: str,
    middle_name: Optional[str],
    last_name: str,
    email: str,
    password: str,
) -> None:
    """Registers a new user."""

    password = crypto.hash_password(email, password)
    print(password)

    user = models.User(
        first_name=first_name,
        middle_name=middle_name or None,
        last_name=last_name,
        email=email,
        password=password,
    )

    user.save()

    LOGGER.info(
        "Created new user",
        id=user.id,
        first_name=first_name,
        middle_name=middle_name or None,
        last_name=last_name,
        email=email,
        passwod=password,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Registers a new user.")

    parser.add_argument(
        "--first-name", dest="first_name", action="store", required=True
    )
    parser.add_argument(
        "--middle-name", dest="middle_name", action="store", default="", required=False
    )
    parser.add_argument("--last-name", dest="last_name", action="store", required=True)
    parser.add_argument("--email", dest="email", action="store", required=True)
    parser.add_argument("--password", dest="password", action="store", required=True)

    args = parser.parse_args()
    register_user(
        args.first_name, args.middle_name, args.last_name, args.email, args.password
    )

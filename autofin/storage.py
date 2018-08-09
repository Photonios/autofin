import os
import structlog

from autofin import settings

from .user import User

LOGGER = structlog.get_logger(__name__)


class Storage:
    """Text-file based persistent storage."""

    USERS_FILENAME = "users.txt"

    def __init__(self):
        """Initializes the storage by reading it back from disk."""

        self._ensure_exists()
        self._users_file_path = os.path.join(settings.STORAGE_PATH, self.USERS_FILENAME)

        self.users = []

        self.read()

    def read(self):
        """Reads from storage into memory."""

        if os.path.isfile(self._users_file_path):
            with open(self._users_file_path, "r") as fp:
                self.users = [User(phone_number) for phone_number in fp.readlines()]

                LOGGER.info(
                    "Read users from storage", count=len(self.users), users=self.users
                )

    def write(self):
        """Writes from memory into storage."""

        with open(self._users_file_path, "w") as fp:
            for user in self.users:
                fp.writeline(user.__repr__())

            LOGGER.info(
                "Wrote users to storage", count=len(self.users), users=self.users
            )

    def _ensure_exists(self):
        """Ensures the storage directory exists."""

        if not os.path.isdir(settings.STORAGE_PATH):
            os.makedirs(settings.STORAGE_PATH)
        LOGGER.info("Verified storage directory", path=settings.STORAGE_PATH)

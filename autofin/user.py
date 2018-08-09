class User:
    """Represents a single Autofin user."""

    def __init__(self, phone_number: str) -> None:
        """Initializes a new instance of :see:User.

        Arguments:
            phone_number:
                The user's phone number to
                send notifications to.
        """

        self.phone_number = phone_number

    def __repr__(self):
        """Gets a textual representation of this user."""

        return self.phone_number

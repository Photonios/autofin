class CreditorImpl:
    """Base class for creditors."""

    def __init__(self) -> None:
        """Initializes a new instance of :see:Creditor with
        the specified name."""

        class Error(RuntimeError):
            """Error that is raised by :see:Creditor implementations."""

            pass

        class AuthError(Error):
            """Error that is raised when authentication failed
            for a creditor."""

            def __init__(_) -> None:
                super().__init__("Authentication failed")

        self.Error = Error
        self.AuthError = AuthError

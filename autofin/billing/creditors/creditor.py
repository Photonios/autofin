from autofin.browser import BrowserManager


class Creditor:
    """Base class for creditors."""

    def __init__(self, name: str) -> None:
        """Initializes a new instance of :see:Creditor with
        the specified name."""

        self.name = name
        self.browser_manager = BrowserManager(self.name)

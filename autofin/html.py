class CSSSelectorCollection:
    """Collection of CSS selectors to use for finding
    elements in a HTML document."""

    def __init__(self, **selectors) -> None:
        """Initializes a new instance of :see:CSSSelectorCollection."""

        for key, value in selectors.items():
            setattr(self, key, value)

from typing import Generator, List, Tuple


class GlorifiedEnum:
    """An enum type that is not a Python3 enum but
    just a class with string constants."""

    @classmethod
    def all(cls) -> List:
        """Gets all possible options from this enum."""
        values = [value for key, value in cls.__dict__.items() if key.isupper()]

        return sorted(values, reverse=True)

    @classmethod
    def choices(cls) -> List[Tuple[str, str]]:
        """Gets a list of tuples describing the possible
        "choices" this enum offers. (name, value)."""
        return [(item, item.title()) for item in cls.all()]

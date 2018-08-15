from peewee import IntegerField

from autofin.util import GlorifiedEnum


class IntegerEnumField(IntegerField):
    """Field for Peewee that allows storing Enum values."""

    def __init__(self, enum: GlorifiedEnum, *args, **kwargs) -> None:
        """Initializes a new instance of :see:IntegerEnumField.

        Arguments:
            enum:
                Enum type this field stores.
        """

        self.enum = enum
        super().__init__(*args, **kwargs)

    def db_value(self, value: int) -> None:
        """Converts the specified DB value to a Python value."""

        if value not in self.enum.all():
            raise TypeError(
                "%s (%s) is not a valid member of %s"
                % (value, type(value), str(self.enum))
            )

        return value

    def python_value(self, value: int) -> None:
        """Convers the specified Python value to a DB value."""

        return value

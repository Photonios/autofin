
from autofin.util import GlorifiedEnum


class CreditorID(GlorifiedEnum):
    """Maps creditor names to ID's."""

    EON_ROMANIA = 0
    UPC_ROMANIA = 1
    DIGI_ROMANIA = 2
    ELECTRICA_ROMANIA = 3

    def human_readable(self, value: int) -> str:
        """Gets a human-readable name for the
        specified name."""

        human_readable_map = {
            self.EON_ROMANIA: "E.ON Romania",
            self.UPC_ROMANIA: "UPC Romania",
            self.DIGI_ROMANIA: "Digi Romania (RDS & RCS)",
            self.ELECTRIA_ROMANI: "Electria SA Romania",
        }

        return value.get(value)

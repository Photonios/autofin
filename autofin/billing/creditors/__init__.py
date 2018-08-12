from autofin import settings
from autofin.util import GlorifiedEnum

from .eon import EON
from .upc import UPC
from .digi import Digi
from .electrica import Electrica


class CreditorName(GlorifiedEnum):
    """Available invoice creditors."""

    EON = "eon"
    UPC = "upc"
    DIGI = "digi"
    ELECTRICA = "electrica"


creditors_class_map = {
    CreditorName.EON: EON,
    CreditorName.UPC: UPC,
    CreditorName.DIGI: Digi,
    CreditorName.ELECTRICA: Electrica,
}

creditors = {
    name: creditors_class_map[name](*credentials)
    for name, credentials in settings.CREDITORS.items()
}

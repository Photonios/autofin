from autofin import settings
from autofin.util import GlorifiedEnum

from .electrica import Electrica


class CreditorName(GlorifiedEnum):
    """Available invoice creditors."""

    EON = "eon"
    UPC = "upc"
    RDS = "rds"
    ELECTRICA = "electrica"


creditors_class_map = {CreditorName.ELECTRICA: Electrica}

creditors = {
    name: creditors_class_map[name](*credentials)
    for name, credentials in settings.CREDITORS.items()
}

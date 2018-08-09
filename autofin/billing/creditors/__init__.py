from autofin.util import GlorifiedEnum

from .electrica import Electrica


class CreditorName(GlorifiedEnum):
    """Available invoice creditors."""

    EON = "eon"
    UPC = "upc"
    RDS = "rds"
    ELECTRICA = "electrica"


creditors = {CreditorName.ELECTRICA: Electrica("adela.suhani@gmail.com", "aoeuid123")}

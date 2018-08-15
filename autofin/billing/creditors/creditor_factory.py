from typing import Tuple

from .eon import EON
from .upc import UPC
from .digi import Digi
from .electrica import Electrica
from .creditor_impl import CreditorImpl
from .creditor_id import CreditorID


class CreditorFactory:
    _map = {
        CreditorID.EON: EON,
        CreditorID.UPC: UPC,
        CreditorID.DIGI: Digi,
        CreditorID.ELECTRICA: Electrica,
    }

    @classmethod
    def new(cls, creditor_id: int, credentials: Tuple[str, str]) -> CreditorImpl:
        """Creates a new instance of a creditor using the
        specified :see:CreditorID."""

        impl = cls._map.get(creditor_id)
        if not impl:
            raise TypeError(
                "%d is not mapped to a creditor implementation" % creditor_id
            )

        return impl(*credentials)

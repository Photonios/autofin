from typing import Tuple

from .creditor_id import CreditorID
from .creditor_impl import CreditorImpl
from .eon_romania import EONRomania
from .upc_romania import UPCRomania
from .digi_romania import DigiRomania
from .electrica_romania import ElectricaRomania


class CreditorFactory:
    _map = {
        CreditorID.EON_ROMANIA: EONRomania,
        CreditorID.UPC_ROMANIA: UPCRomania,
        CreditorID.DIGI_ROMANIA: DigiRomania,
        CreditorID.ELECTRICA_ROMANIA: ElectricaRomania,
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

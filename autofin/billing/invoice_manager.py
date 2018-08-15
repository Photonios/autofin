from typing import List

from concurrent.futures import ThreadPoolExecutor

from autofin import models

from .invoice import Invoice
from .creditors import CreditorFactory


class InvoiceManager:
    """Helps managing invoices by retrieving information
    from creditors."""

    def __init__(self, user: models.User) -> None:
        """Initializes a new :see:InvoiceManager for the
        specified user."""

        self.user = user

    def get_latest_invoices(self) -> List[Invoice]:
        """Gets the last invoice, paid or not from all
        registered creditors."""

        futures = []

        creditor_count = len(self.user.creditors)
        with ThreadPoolExecutor(max_workers=creditor_count) as pool:
            for creditor_config in self.user.creditors:
                creditor_impl = CreditorFactory.new(
                    creditor_config.creditor.id,
                    (creditor_config.username, creditor_config.password),
                )
                futures.append(pool.submit(creditor_impl.get_latest_invoice))

        invoices = [future.result() for future in futures]
        return invoices

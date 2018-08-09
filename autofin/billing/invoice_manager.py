from typing import List

from autofin.billing.creditors import creditors

from .invoice import Invoice


class InvoiceManager:
    """Helps managing invoices by retrieving information
    from creditors."""

    def get_latest_invoices(self) -> List[Invoice]:
        """Gets the last invoice, paid or not from all
        registered creditors."""

        invoices = [creditor.get_latest_invoice() for _, creditor in creditors.items()]

        return invoices

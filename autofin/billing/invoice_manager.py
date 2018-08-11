from typing import List

from concurrent.futures import ThreadPoolExecutor
from autofin.billing.creditors import creditors

from .invoice import Invoice


class InvoiceManager:
    """Helps managing invoices by retrieving information
    from creditors."""

    def get_latest_invoices(self) -> List[Invoice]:
        """Gets the last invoice, paid or not from all
        registered creditors."""

        futures = []
        with ThreadPoolExecutor(max_workers=len(creditors)) as pool:
            for _, creditor in creditors.items():
                futures.append(pool.submit(creditor.get_latest_invoice))

        invoices = [future.result() for future in futures]

        return invoices

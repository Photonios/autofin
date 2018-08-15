import bs4
import structlog

from datetime import datetime

from autofin import http, html
from autofin.billing import PaymentStatus, Invoice

from .creditor_impl import CreditorImpl

LOGGER = structlog.get_logger(__name__)


class Electrica(CreditorImpl):
    """Provides access to Electrica bills."""

    def __init__(self, email: str, password: str) -> None:
        """Initializes a new instance of :see:Electrica."""

        super().__init__("Electrica SRL")

        self._email = email
        self._password = password

        self._login_url = (
            "https://myelectrica.ro/modules/login/form-processors/login.processor.php"
        )
        self._invoices_url = "https://myelectrica.ro/index.php?pagina=facturile-mele"

        self._selectors = html.CSSSelectorCollection(
            current_user=".profile-info",
            invoice_date="#datatable-facturi tbody tr:nth-of-type(1) td:nth-of-type(2)",
            invoice_due_date="#datatable-facturi tbody tr:nth-of-type(1) td:nth-of-type(3)",
            invoice_payment_status="#datatable-facturi tbody tr:nth-of-type(1) td:nth-of-type(5)",
            invoice_amount="#datatable-facturi tbody tr:nth-of-type(1) td:nth-of-type(6)",
        )

    def get_latest_invoice(self) -> Invoice:
        """Gets the latest bill, paid or not paid."""

        LOGGER.info("Getting latest invoice from Electrica")

        session = http.create_session()

        login_data = {
            "myelectrica_utilizator": self._email,
            "myelectrica_pass": self._password,
            "myelectrica_login_btn": "",
        }

        if session.post(self._login_url, login_data).status_code != 200:
            raise self.AuthError()

        response = session.get(self._invoices_url)
        if response.status_code != 200:
            raise self.Error("Failed to get list of invoices")

        soup = bs4.BeautifulSoup(response.content, "html.parser")
        if not soup.select_one(self._selectors.current_user):
            raise self.AuthError()

        invoice_date_elem = soup.select_one(self._selectors.invoice_date)
        if not invoice_date_elem:
            raise self.Error("Failed to get invoice date")

        invoice_due_date_elem = soup.select_one(self._selectors.invoice_due_date)
        if not invoice_due_date_elem:
            raise self.Error("Failed to get invoice due date")

        invoice_payment_status_elem = soup.select_one(
            self._selectors.invoice_payment_status
        )
        if not invoice_payment_status_elem:
            raise self.Error("Failed to get invoice payment status")

        invoice_amount_elem = soup.select_one(self._selectors.invoice_amount)
        if not invoice_amount_elem:
            raise self.Error("Failed to get invoice amount")

        invoice_date = int(invoice_date_elem.get("data-order"))
        invoice_due_date = int(invoice_due_date_elem.get("data-order"))
        invoice_payment_status = invoice_payment_status_elem.text
        invoice_amount = float(invoice_amount_elem.text.replace(",", "."))

        invoice = Invoice(
            self.name,
            invoice_amount,
            datetime.fromtimestamp(invoice_date),
            datetime.fromtimestamp(invoice_due_date),
            PaymentStatus.PAID_CONFIRMED
            if invoice_payment_status == "Incasata"
            else PaymentStatus.UNPAID,
        )

        LOGGER.info("Found latest Electria invoice", invoice=invoice)
        return invoice

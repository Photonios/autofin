import bs4
import structlog

from datetime import datetime

from autofin import http, html, models
from autofin.billing import Currency, PaymentStatus

from .creditor_impl import CreditorImpl
from .creditor_invoice import CreditorInvoice

LOGGER = structlog.get_logger(__name__)


class EONRomania(CreditorImpl):
    """Provides access to EON Romania bills."""

    def __init__(self, email: str, password: str) -> None:
        """Initializes a new instance of :see:EONRomania."""

        self._email = email
        self._password = password

        self._login_page_url = "https://myline-eon.ro/login"
        self._login_url = "https://myline-eon.ro/login-check"
        self._invoices_url = "https://myline-eon.ro/facturile-mele"

        self._selectors = html.CSSSelectorCollection(
            sidebar="#sidebar",
            invoice_date="ul.invoices li:nth-of-type(2) div.eon-table-heading",
            invoice_due_date="ul.invoices li:nth-of-type(2) div.eon-table-content div:nth-of-type(1)",
            invoice_payment_status="ul.invoices li:nth-of-type(2) div.eon-table-content div:nth-of-type(4)",
            invoice_amount="ul.invoices li:nth-of-type(2) div.eon-table-content div:nth-of-type(3)",
        )

    def get_latest_invoice(self) -> CreditorInvoice:
        """Gets the latest bill, paid or not paid."""

        LOGGER.info("Getting latest invoice from EON Romania")

        session = http.create_session()

        response = session.get(self._login_page_url)
        if response.status_code != 200:
            raise self.Error("Login page is not functioning")

        soup = bs4.BeautifulSoup(response.content, "html.parser")
        csrf_token_elem = soup.find("input", {"name": "_csrf_token"})
        if not csrf_token_elem:
            raise self.Error("Could not extract CSRF token")

        login_data = {
            "_username": self._email,
            "_password": self._password,
            "_csrf_token": csrf_token_elem.get("value"),
        }

        if session.post(self._login_url, login_data).status_code != 200:
            raise self.AuthError()

        response = session.get(self._invoices_url)
        soup = bs4.BeautifulSoup(response.content, "html.parser")

        if not soup.select_one(self._selectors.sidebar):
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

        invoice_date = invoice_date_elem.contents[-1]
        invoice_due_date = invoice_due_date_elem.contents[-1]
        invoice_payment_status = invoice_payment_status_elem.contents[-1]
        invoice_amount = invoice_amount_elem.contents[-1]

        invoice = CreditorInvoice(
            float(invoice_amount.replace(",", ".")),
            Currency.RON,
            datetime.strptime(invoice_date, "%d.%m.%Y"),
            datetime.strptime(invoice_due_date, "%d.%m.%Y"),
            PaymentStatus.PAID_CONFIRMED
            if invoice_payment_status == "0.00"
            else PaymentStatus.UNPAID,
        )

        LOGGER.info("Found latest EON Romania invoice", invoice=invoice)
        return invoice

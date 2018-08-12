import bs4
import structlog

from datetime import datetime

from autofin import http, html
from autofin.billing import PaymentStatus, Invoice

from .creditor import Creditor

LOGGER = structlog.get_logger(__name__)


class Digi(Creditor):
    """Provides access to Digi bills."""

    def __init__(self, email: str, password: str) -> None:
        """Initializes a new instance of :see:Digi."""

        super().__init__("Digi")

        self._email = email
        self._password = password

        self._login_url = "https://www.digiromania.ro/auth/login"
        self._invoices_url = "https://www.digiromania.ro/my-account/invoices"
        self._single_invoice_url = (
            "https://www.digiromania.ro/my-account/invoices/details?invoice_id="
        )

        self._selectors = html.CSSSelectorCollection(
            invoices=".invoice-table .invoice-details",
            invoice_date="h4",
            invoice_due_date=".due-date",
            invoice_amount=".value",
            invoice_payment_status=".remaining",
        )

    def get_latest_invoice(self) -> Invoice:
        """Gets the latest bill, paid or not paid."""

        LOGGER.info("Getting latest invoice from Digi")

        session = http.create_session()

        login_data = {
            "signin-input-email": self._email,
            "signin-input-password": self._password,
            "signin-submit-button": "",
        }

        if (
            session.post(self._login_url, login_data, allow_redirects=False).status_code
            != 302
        ):
            raise self.AuthError()

        response = session.get(self._invoices_url)
        soup = bs4.BeautifulSoup(response.content, "html.parser")

        invoice_elem = soup.select_one(self._selectors.invoices)
        if not invoice_elem:
            raise self.AuthError()

        invoice_due_date_elem = invoice_elem.select_one(
            self._selectors.invoice_due_date
        )
        if not invoice_due_date_elem:
            raise self.Error("Failed to get invoice due date")

        invoice_payment_status_elem = invoice_elem.select_one(
            self._selectors.invoice_payment_status
        )
        if not invoice_payment_status_elem:
            raise self.Error("Failed to get invoice payment status")

        invoice_amount_elem = invoice_elem.select_one(self._selectors.invoice_amount)
        if not invoice_amount_elem:
            raise self.Error("Failed to get invoice amount")

        invoice_id = invoice_elem.get("data-invoice-id")
        if not invoice_id:
            raise self.Error("Could not get invoice ID")

        response = session.get(self._single_invoice_url + invoice_id)
        soup = bs4.BeautifulSoup(response.content, "html.parser")

        invoice_date_elem = soup.select_one(self._selectors.invoice_date)
        if not invoice_date_elem:
            raise self.Error("Failed to get invoice date")

        invoice_date = invoice_date_elem.contents[-1].replace("din data de ", "")
        invoice_due_date = invoice_due_date_elem.text.strip()
        invoice_payment_status = invoice_payment_status_elem.text.strip()
        invoice_amount = invoice_amount_elem.text.strip()

        invoice = Invoice(
            self.name,
            float(
                invoice_amount.replace(" lei", ".").replace("&period", ".").rstrip(".")
            ),
            datetime.strptime(invoice_date, "%d-%m-%Y"),
            datetime.strptime(invoice_due_date, "%d-%m-%Y"),
            PaymentStatus.PAID_CONFIRMED
            if invoice_payment_status.replace(" lei", "") == "0&period;00 lei"
            else PaymentStatus.UNPAID,
        )

        LOGGER.info("Found latest Digi invoice", invoice=invoice)
        return invoice

import bs4
import structlog

from datetime import datetime

from autofin import http, html
from autofin.billing import Currency, PaymentStatus

from .creditor_impl import CreditorImpl
from .creditor_invoice import CreditorInvoice

LOGGER = structlog.get_logger(__name__)


class UPCRomania(CreditorImpl):
    """Provides access to UPC Romania bills."""

    def __init__(self, email: str, password: str) -> None:
        """Initializes a new instance of :see:UPCRomania."""

        self._email = email
        self._password = password

        self._selectors = html.CSSSelectorCollection(
            current_user=".navbar-account",
            invoice_date="#facturi tr:nth-of-type(1) td:nth-of-type(3) p.invoices-table__value",
            invoice_due_date="#facturi tr:nth-of-type(1) td:nth-of-type(4) p.invoices-table__value",
            invoice_payment_status="#facturi tr:nth-of-type(1) td:nth-of-type(5) p.invoices-table__value",
            invoice_amount="#facturi tr:nth-of-type(1) td:nth-of-type(6) p.invoices-table__value",
        )

        self._login_page_url = "https://my.upc.ro/myupc-web/appmanager/portal"
        self._login_url = "https://my.upc.ro/myupc-web/appmanager/portal/guest?_nfpb=true&_st=&_windowLabel=login_v2_portlet&_urlType=action&wlplogin_v2_portlet_action=submitForm"
        self._invoices_url = "https://my.upc.ro/myupc-web/appmanager/portal/home?_nfpb=true&_st=&_pageLabel=BillDefaultPage_v2#facturi"

    def get_latest_invoice(self) -> CreditorInvoice:
        """Gets the latest bill, paid or not paid."""

        LOGGER.info("Getting latest invoice from UPC Romania")

        session = http.create_session()

        response = session.get(self._login_page_url)
        if response.status_code != 200:
            raise self.Error("Login page is not functioning")

        soup = bs4.BeautifulSoup(response.content, "html.parser")
        csrf_token_elem = soup.find("input", {"name": "csrfToken"})
        if not csrf_token_elem:
            raise self.Error("Could not extract CSRF token")

        login_data = {
            "inputEmail": self._email,
            "password": self._password,
            "csrfToken": csrf_token_elem.get("value"),
            "errorsinput": "",
        }

        response = session.post(self._login_url, login_data)
        soup = bs4.BeautifulSoup(response.content, "html.parser")
        if not soup.select_one(self._selectors.current_user):
            raise self.AuthError()

        response = session.get(self._invoices_url)
        soup = bs4.BeautifulSoup(response.content, "html.parser")

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

        invoice_date = invoice_date_elem.text.strip()
        invoice_due_date = invoice_due_date_elem.text.strip()
        invoice_payment_status = invoice_payment_status_elem.text.strip()
        invoice_amount = invoice_amount_elem.text.strip()

        invoice = CreditorInvoice(
            float(invoice_amount.replace(" LEI", "")),
            Currency.RON,
            datetime.strptime(invoice_date, "%d.%m.%Y"),
            datetime.strptime(invoice_due_date, "%d.%m.%Y"),
            PaymentStatus.PAID_CONFIRMED
            if invoice_payment_status == "Efectuată"
            else PaymentStatus.UNPAID,
        )

        LOGGER.info("Found latest UPC Romania invoice", invoice=invoice)
        return invoice

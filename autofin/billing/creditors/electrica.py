import structlog

from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from autofin.billing import PaymentStatus, Invoice

from .creditor import Creditor

LOGGER = structlog.get_logger(__name__)


class Electrica(Creditor):
    """Provides access to Electrica bills."""

    LOGIN_URL = "https://myelectrica.ro/index.php?pagina=login"
    INVOICES_URL = "https://myelectrica.ro/index.php?pagina=facturile-mele"
    SELECTORS = {
        "email_input": (By.CSS_SELECTOR, "#myelectrica_utilizator"),
        "password_input": (By.CSS_SELECTOR, "#myelectrica_pass"),
        "current_user": (By.CSS_SELECTOR, ".profile-info"),
        "invoice_date": (
            By.CSS_SELECTOR,
            "#datatable-facturi tbody tr:nth-child(1) td:nth-child(2)",
        ),
        "invoice_due_date": (
            By.CSS_SELECTOR,
            "#datatable-facturi tbody tr:nth-child(1) td:nth-child(3)",
        ),
        "invoice_payment_status": (
            By.CSS_SELECTOR,
            "#datatable-facturi tbody tr:nth-child(1) td:nth-child(5)",
        ),
        "invoice_amount": (
            By.CSS_SELECTOR,
            "#datatable-facturi tbody tr:nth-child(1) td:nth-child(6)",
        ),
    }

    def __init__(self, email: str, password: str) -> None:
        """Initializes a new instance of :see:Electrica."""

        super().__init__("Electrica SRL")

        self._email = email
        self._password = password

    def get_latest_invoice(self) -> Invoice:
        """Gets the latest bill, paid or not paid."""

        LOGGER.info("Getting latest invoice from Electrica")

        browser = self.browser_manager.create_browser()
        browser.get(self.INVOICES_URL)

        try:
            WebDriverWait(browser, 2).until(
                EC.presence_of_element_located(self.SELECTORS["current_user"])
            )

            LOGGER.debug("Already logged into Electrica, skipping login")
        except Exception:
            LOGGER.debug("Logging into Electrica", url=self.LOGIN_URL)
            browser.get(self.LOGIN_URL)

            email_input = browser.find_element(*self.SELECTORS["email_input"])
            password_input = browser.find_element(*self.SELECTORS["password_input"])

            email_input.send_keys(self._email)
            password_input.send_keys(self._password)
            password_input.send_keys(Keys.ENTER)

            LOGGER.debug(
                "Navigating to invoices section for Electrica", url=self.INVOICES_URL
            )

            browser.get(self.INVOICES_URL)

        invoice_date_elem = browser.find_element(*self.SELECTORS["invoice_date"])
        invoice_due_date_elem = browser.find_element(
            *self.SELECTORS["invoice_due_date"]
        )
        invoice_payment_status_elem = browser.find_element(
            *self.SELECTORS["invoice_payment_status"]
        )
        invoice_amount_elem = browser.find_element(*self.SELECTORS["invoice_amount"])

        invoice_date = int(invoice_date_elem.get_attribute("data-order"))
        invoice_due_date = int(invoice_due_date_elem.get_attribute("data-order"))
        invoice_payment_status = invoice_payment_status_elem.text
        invoice_amount = float(invoice_amount_elem.text.replace(",", "."))

        self.browser_manager.destroy_browser()

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

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


class EON(Creditor):
    """Provides access to EON bills."""

    LOGIN_URL = "https://myline-eon.ro/login"
    INVOICES_URL = "https://myline-eon.ro/facturile-mele"
    SELECTORS = {
        "email_input": (By.CSS_SELECTOR, "#username"),
        "password_input": (By.CSS_SELECTOR, "#password"),
        "sidebar": (By.CSS_SELECTOR, ".eon-sidebar"),
        "lastest_invoice_row": (By.CSS_SELECTOR, "ul.invoices li.invoice:nth-child(2)"),
        "invoice_date": (
            By.CSS_SELECTOR,
            "ul.invoices li.invoice:nth-child(2) div.eon-table-heading",
        ),
        "invoice_due_date": (
            By.CSS_SELECTOR,
            "ul.invoices li.invoice:nth-child(2) div.eon-table-content div:nth-child(1)",
        ),
        "invoice_payment_status": (
            By.CSS_SELECTOR,
            "ul.invoices li.invoice:nth-child(2) div.eon-table-content div:nth-child(4)",
        ),
        "invoice_amount": (
            By.CSS_SELECTOR,
            "ul.invoices li.invoice:nth-child(2) div.eon-table-content div:nth-child(3)",
        ),
    }

    def __init__(self, email: str, password: str) -> None:
        """Initializes a new instance of :see:EON."""

        super().__init__("E-on")

        self._email = email
        self._password = password

    def get_latest_invoice(self) -> Invoice:
        """Gets the latest bill, paid or not paid."""

        LOGGER.info("Getting latest invoice from EON")

        browser = self.browser_manager.create_browser()
        browser.get(self.INVOICES_URL)

        try:
            WebDriverWait(browser, 2).until(
                EC.presence_of_element_located(self.SELECTORS["sidebar"])
            )

            LOGGER.debug("Already logged into EON, skipping login")
        except Exception:
            LOGGER.debug("Logging into EON", url=self.LOGIN_URL)

            browser.get(self.LOGIN_URL)

            email_input = browser.find_element(*self.SELECTORS["email_input"])
            password_input = browser.find_element(*self.SELECTORS["password_input"])

            email_input.send_keys(self._email)
            password_input.send_keys(self._password)
            password_input.send_keys(Keys.ENTER)

            LOGGER.debug(
                "Navigating to invoices section for EON", url=self.INVOICES_URL
            )
            browser.get(self.INVOICES_URL)

        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located(self.SELECTORS["lastest_invoice_row"])
        )

        invoice_date_elem = browser.find_element(*self.SELECTORS["invoice_date"])
        invoice_due_date_elem = browser.find_element(
            *self.SELECTORS["invoice_due_date"]
        )
        invoice_payment_status_elem = browser.find_element(
            *self.SELECTORS["invoice_payment_status"]
        )
        invoice_amount_elem = browser.find_element(*self.SELECTORS["invoice_amount"])

        invoice_date = invoice_date_elem.text
        invoice_due_date = invoice_due_date_elem.text
        invoice_payment_status = invoice_payment_status_elem.text
        invoice_amount = invoice_amount_elem.text

        self.browser_manager.destroy_browser()

        invoice = Invoice(
            self.name,
            float(invoice_amount.replace(",", ".")),
            datetime.strptime(invoice_date, "%d.%m.%Y"),
            datetime.strptime(invoice_due_date, "%d.%m.%Y"),
            PaymentStatus.PAID_CONFIRMED
            if invoice_payment_status == "0.00"
            else PaymentStatus.UNPAID,
        )

        LOGGER.info("Found latest EON invoice", invoice=invoice)
        return invoice

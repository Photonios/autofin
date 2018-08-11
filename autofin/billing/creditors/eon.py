import structlog

from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from autofin import selenium
from autofin.billing import PaymentStatus, Invoice

LOGGER = structlog.get_logger(__name__)


class EON:
    """Provides access to EON bills."""

    NAME = "E-on"
    LOGIN_URL = "https://myline-eon.ro/login"
    INVOICES_URL = "https://myline-eon.ro/facturile-mele"
    SELECTORS = {
        "email_input": (By.CSS_SELECTOR, "#username"),
        "password_input": (By.CSS_SELECTOR, "#password"),
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

        self._email = email
        self._password = password

    def get_latest_invoice(self) -> Invoice:
        """Gets the latest bill, paid or not paid."""

        LOGGER.info("Getting latest invoice from EON")

        browser = selenium.create_browser()
        browser.get(self.LOGIN_URL)

        LOGGER.debug("Logging into EON", url=self.LOGIN_URL)

        email_input = browser.find_element(*self.SELECTORS["email_input"])
        password_input = browser.find_element(*self.SELECTORS["password_input"])

        email_input.send_keys(self._email)
        password_input.send_keys(self._password)
        password_input.send_keys(Keys.ENTER)

        LOGGER.debug("Navigating to invoices section for EON", url=self.INVOICES_URL)

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

        browser.close()

        invoice = Invoice(
            self.NAME,
            float(invoice_amount.replace(",", ".")),
            datetime.strptime(invoice_date, "%d.%m.%Y"),
            datetime.strptime(invoice_due_date, "%d.%m.%Y"),
            PaymentStatus.PAID_CONFIRMED
            if invoice_payment_status == "0.00"
            else PaymentStatus.UNPAID,
        )

        LOGGER.info("Found latest Electria invoice", invoice=invoice)
        return invoice

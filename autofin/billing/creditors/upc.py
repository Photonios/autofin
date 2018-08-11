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


class UPC(Creditor):
    """Provides access to UPC bills."""

    LOGIN_URL = "https://my.upc.ro/myupc-web/appmanager/portal"
    INVOICES_URL = "https://my.upc.ro/myupc-web/appmanager/portal/home?_nfpb=true&_st=&_pageLabel=BillDefaultPage_v2#facturi"
    SELECTORS = {
        "email_input": (By.CSS_SELECTOR, "#inputEmail"),
        "password_input": (By.CSS_SELECTOR, "#password"),
        "current_user": (By.CSS_SELECTOR, ".navbar-account"),
        "invoice_date": (
            By.CSS_SELECTOR,
            "#facturi tr:nth-child(1) td:nth-child(3) p.invoices-table__value",
        ),
        "invoice_due_date": (
            By.CSS_SELECTOR,
            "#facturi tr:nth-child(1) td:nth-child(4) p.invoices-table__value",
        ),
        "invoice_payment_status": (
            By.CSS_SELECTOR,
            "#facturi tr:nth-child(1) td:nth-child(5) p.invoices-table__value",
        ),
        "invoice_amount": (
            By.CSS_SELECTOR,
            "#facturi tr:nth-child(1) td:nth-child(6) p.invoices-table__value",
        ),
    }

    def __init__(self, email: str, password: str) -> None:
        """Initializes a new instance of :see:UPC."""

        super().__init__("UPC")

        self._email = email
        self._password = password

    def get_latest_invoice(self) -> Invoice:
        """Gets the latest bill, paid or not paid."""

        LOGGER.info("Getting latest invoice from UPC")

        browser = self.browser_manager.create_browser()
        browser.get(self.INVOICES_URL)

        try:
            WebDriverWait(browser, 2).until(
                EC.presence_of_element_located(self.SELECTORS["current_user"])
            )

            LOGGER.debug("Already logged into UPC, skipping login")
        except Exception:
            LOGGER.debug("Logging into UPC", url=self.LOGIN_URL)

            browser.get(self.LOGIN_URL)

            email_input = browser.find_element(*self.SELECTORS["email_input"])
            password_input = browser.find_element(*self.SELECTORS["password_input"])

            email_input.send_keys(self._email)
            password_input.send_keys(self._password)
            password_input.send_keys(Keys.ENTER)

            LOGGER.debug(
                "Navigating to invoices section for UPC", url=self.INVOICES_URL
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

        invoice_date = invoice_date_elem.text
        invoice_due_date = invoice_due_date_elem.text
        invoice_payment_status = invoice_payment_status_elem.text
        invoice_amount = invoice_amount_elem.text

        self.browser_manager.destroy_browser()

        invoice = Invoice(
            self.name,
            float(invoice_amount.replace(" LEI", "")),
            datetime.strptime(invoice_date, "%d.%m.%Y"),
            datetime.strptime(invoice_due_date, "%d.%m.%Y"),
            PaymentStatus.PAID_CONFIRMED
            if invoice_payment_status == "Efectuată"
            else PaymentStatus.UNPAID,
        )

        LOGGER.info("Found latest UPC invoice", invoice=invoice)
        return invoice

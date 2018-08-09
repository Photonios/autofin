from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from autofin.billing import PaymentStatus, Invoice


class Electrica:
    """Provides access to Electrica bills."""

    NAME = "Electrica SRL"
    LOGIN_URL = "https://myelectrica.ro/index.php?pagina=login"
    INVOICES_URL = "https://myelectrica.ro/index.php?pagina=facturile-mele"
    SELECTORS = {
        "email_input": (By.CSS_SELECTOR, "#myelectrica_utilizator"),
        "password_input": (By.CSS_SELECTOR, "#myelectrica_pass"),
        "campaign_close_button": (By.CSS_SELECTOR, ".modal .modal-header .close"),
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
        """Initializes a new instance of :see:ElectricaCreditor."""

        self._email = email
        self._password = password

    def get_latest_invoice(self) -> Invoice:
        """Gets the latest bill, paid or not paid."""

        browser = webdriver.Chrome()
        browser.get(self.LOGIN_URL)

        email_input = browser.find_element(*self.SELECTORS["email_input"])
        password_input = browser.find_element(*self.SELECTORS["password_input"])

        email_input.send_keys(self._email)
        password_input.send_keys(self._password)
        password_input.send_keys(Keys.ENTER)

        browser.get(self.INVOICES_URL)

        invoice_date = int(
            browser.find_element(*self.SELECTORS["invoice_date"]).get_attribute(
                "data-order"
            )
        )
        invoice_due_date = int(
            browser.find_element(*self.SELECTORS["invoice_due_date"]).get_attribute(
                "data-order"
            )
        )
        invoice_payment_status = browser.find_element(
            *self.SELECTORS["invoice_payment_status"]
        ).text
        invoice_amount = float(
            browser.find_element(*self.SELECTORS["invoice_amount"]).text.replace(
                ",", "."
            )
        )

        browser.close()

        invoice = Invoice(
            self.NAME,
            invoice_amount,
            datetime.fromtimestamp(invoice_date),
            datetime.fromtimestamp(invoice_due_date),
            PaymentStatus.PAID_CONFIRMED
            if invoice_payment_status == "Incasata"
            else PaymentStatus.UNPAID,
        )

        return invoice

from decimal import Decimal

from selenium.webdriver.common.by import By

from data.saucedemo import Customer
from framework.base_page import BasePage
from pages.saucedemo.prices import parse_price


class CheckoutInformationPage(BasePage):
    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    ERROR = (By.CSS_SELECTOR, "[data-test='error']")

    def continue_with(self, customer: Customer) -> "CheckoutOverviewPage":
        self._fill(customer)
        return CheckoutOverviewPage(self.driver)

    def attempt_continue_with(self, customer: Customer) -> "CheckoutInformationPage":
        """Envía el formulario esperando un error de validación."""
        self._fill(customer)
        return self

    def error_message(self) -> str:
        return self.text_of(self.ERROR)

    def _fill(self, customer: Customer) -> None:
        self.step("Fill customer information and continue")
        self.type(self.FIRST_NAME, customer.first_name)
        self.type(self.LAST_NAME, customer.last_name)
        self.type(self.POSTAL_CODE, customer.postal_code)
        self.click(self.CONTINUE_BUTTON)


class CheckoutOverviewPage(BasePage):
    ITEM_PRICE = (By.CLASS_NAME, "inventory_item_price")
    SUBTOTAL = (By.CLASS_NAME, "summary_subtotal_label")
    TAX = (By.CLASS_NAME, "summary_tax_label")
    TOTAL = (By.CLASS_NAME, "summary_total_label")
    FINISH_BUTTON = (By.ID, "finish")

    def item_prices(self) -> list[Decimal]:
        return [parse_price(text) for text in self.texts_of(self.ITEM_PRICE)]

    def subtotal(self) -> Decimal:
        return parse_price(self.text_of(self.SUBTOTAL))

    def tax(self) -> Decimal:
        return parse_price(self.text_of(self.TAX))

    def total(self) -> Decimal:
        return parse_price(self.text_of(self.TOTAL))

    def finish(self) -> "CheckoutCompletePage":
        self.step("Finish order")
        self.click(self.FINISH_BUTTON)
        return CheckoutCompletePage(self.driver)


class CheckoutCompletePage(BasePage):
    CONFIRMATION_HEADER = (By.CLASS_NAME, "complete-header")

    def confirmation_message(self) -> str:
        return self.text_of(self.CONFIRMATION_HEADER)

from selenium.webdriver.common.by import By

from framework.base_page import BasePage
from pages.saucedemo.checkout_pages import CheckoutInformationPage
from pages.saucedemo.header_component import HeaderComponent


class CartPage(BasePage):
    CART_ITEM = (By.CLASS_NAME, "cart_item")
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    CHECKOUT_BUTTON = (By.ID, "checkout")

    @property
    def header(self) -> HeaderComponent:
        return HeaderComponent(self.driver)

    def item_names(self) -> list[str]:
        self.visible(self.CHECKOUT_BUTTON)
        return self.texts_of(self.ITEM_NAME) if self.is_present(self.CART_ITEM) else []

    def checkout(self) -> CheckoutInformationPage:
        self.step("Proceed to checkout")
        self.click(self.CHECKOUT_BUTTON)
        return CheckoutInformationPage(self.driver)

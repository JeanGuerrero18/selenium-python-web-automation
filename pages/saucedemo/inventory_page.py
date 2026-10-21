from decimal import Decimal
from enum import Enum

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select

from framework.base_page import BasePage
from pages.saucedemo.header_component import HeaderComponent
from pages.saucedemo.prices import parse_price


class SortOption(Enum):
    NAME_A_TO_Z = "az"
    NAME_Z_TO_A = "za"
    PRICE_LOW_TO_HIGH = "lohi"
    PRICE_HIGH_TO_LOW = "hilo"


class InventoryPage(BasePage):
    TITLE = (By.CLASS_NAME, "title")
    ITEM = (By.CLASS_NAME, "inventory_item")
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICE = (By.CLASS_NAME, "inventory_item_price")
    ITEM_BUTTON = (By.TAG_NAME, "button")
    SORT_SELECT = (By.CLASS_NAME, "product_sort_container")

    @property
    def header(self) -> HeaderComponent:
        return HeaderComponent(self.driver)

    def title(self) -> str:
        return self.text_of(self.TITLE)

    def product_names(self) -> list[str]:
        return self.texts_of(self.ITEM_NAME)

    def product_prices(self) -> list[Decimal]:
        return [parse_price(text) for text in self.texts_of(self.ITEM_PRICE)]

    def sort_by(self, option: SortOption) -> "InventoryPage":
        self.step(f"Sort products by {option.name}")
        Select(self.visible(self.SORT_SELECT)).select_by_value(option.value)
        return self

    def add_to_cart(self, product_name: str) -> "InventoryPage":
        """El botón de la tarjeta alterna entre "Add to cart" y "Remove"."""
        self.step(f"Add '{product_name}' to cart")
        self._item_card(product_name).find_element(*self.ITEM_BUTTON).click()
        return self

    def remove_from_cart(self, product_name: str) -> "InventoryPage":
        self.step(f"Remove '{product_name}' from cart")
        self._item_card(product_name).find_element(*self.ITEM_BUTTON).click()
        return self

    def _item_card(self, product_name: str) -> WebElement:
        """Busca la tarjeta de un producto por su nombre visible en lugar de depender de ids generados."""
        for card in self.all_visible(self.ITEM):
            if card.find_element(*self.ITEM_NAME).text.strip() == product_name:
                return card
        raise NoSuchElementException(f"Product not found: {product_name}")

from __future__ import annotations

from typing import TYPE_CHECKING

from selenium.webdriver.common.by import By

from framework.base_page import BasePage

if TYPE_CHECKING:
    from pages.saucedemo.cart_page import CartPage
    from pages.saucedemo.login_page import LoginPage


class HeaderComponent(BasePage):
    """Cabecera común a todas las páginas tras el login: badge y enlace del carrito, y menú lateral."""

    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")

    def cart_count(self) -> int:
        """Número de artículos en el icono del carrito; con el carrito vacío el badge no se renderiza."""
        return int(self.text_of(self.CART_BADGE)) if self.is_present(self.CART_BADGE) else 0

    def open_cart(self) -> CartPage:
        from pages.saucedemo.cart_page import CartPage

        self.step("Open cart")
        self.click(self.CART_LINK)
        return CartPage(self.driver)

    def logout(self) -> LoginPage:
        from pages.saucedemo.login_page import LoginPage

        self.step("Log out from side menu")
        self.click(self.MENU_BUTTON)
        self.click(self.LOGOUT_LINK)
        return LoginPage(self.driver)

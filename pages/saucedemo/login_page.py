from selenium.webdriver.common.by import By

from framework import config
from framework.base_page import BasePage
from pages.saucedemo.inventory_page import InventoryPage


class LoginPage(BasePage):
    USERNAME = (By.ID, "user-name")
    PASSWORD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR = (By.CSS_SELECTOR, "[data-test='error']")

    def open(self) -> "LoginPage":
        self.step("Open SauceDemo login page")
        self.driver.get(config.get("saucedemo.url"))
        self.visible(self.USERNAME)
        return self

    def login_as(self, username: str, password: str) -> InventoryPage:
        self._submit(username, password)
        return InventoryPage(self.driver)

    def attempt_login(self, username: str, password: str) -> "LoginPage":
        """Envía las credenciales esperando quedarse en la página de login (casos negativos)."""
        self._submit(username, password)
        return self

    def error_message(self) -> str:
        return self.text_of(self.ERROR)

    def is_displayed(self) -> bool:
        return self.visible(self.LOGIN_BUTTON).is_displayed()

    def _submit(self, username: str, password: str) -> None:
        # La contraseña nunca se escribe en los logs ni en el reporte.
        self.step(f"Log in with username '{username}'")
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        self.click(self.LOGIN_BUTTON)

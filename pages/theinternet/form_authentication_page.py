from selenium.webdriver.common.by import By

from pages.theinternet.the_internet_page import TheInternetPage


class FormAuthenticationPage(TheInternetPage):
    USERNAME = (By.ID, "username")
    PASSWORD = (By.ID, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "#login button[type='submit']")
    FLASH = (By.ID, "flash")
    SECURE_AREA_HEADER = (By.CSS_SELECTOR, "#content h2")

    def open(self) -> "FormAuthenticationPage":
        self.open_path("/login")
        self.visible(self.USERNAME)
        return self

    def login(self, username: str, password: str) -> "FormAuthenticationPage":
        self.step(f"Log in with username '{username}'")
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        self.click(self.LOGIN_BUTTON)
        return self

    def flash_message(self) -> str:
        """Texto del banner flash sin el símbolo de cierre final."""
        return self.text_of(self.FLASH).replace("×", "").strip()

    def header(self) -> str:
        return self.text_of(self.SECURE_AREA_HEADER)

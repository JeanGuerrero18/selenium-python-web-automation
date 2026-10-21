from selenium.webdriver.common.by import By

from pages.theinternet.the_internet_page import TheInternetPage


class DynamicLoadingPage(TheInternetPage):
    """Ejemplo 2: el elemento de resultado solo se agrega al DOM tras una carga simulada de ~5 s."""

    START_BUTTON = (By.CSS_SELECTOR, "#start button")
    FINISH_TEXT = (By.CSS_SELECTOR, "#finish h4")

    def open(self) -> "DynamicLoadingPage":
        self.open_path("/dynamic_loading/2")
        return self

    def start(self) -> "DynamicLoadingPage":
        self.step("Start loading")
        self.click(self.START_BUTTON)
        return self

    def loaded_text(self) -> str:
        """Espera explícita a que aparezca el elemento; sin time.sleep."""
        return self.text_of(self.FINISH_TEXT)

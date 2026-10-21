"""Comportamiento común de los page objects.

Cada interacción pasa por una espera explícita; nunca se configuran esperas implícitas,
así que ambas no se combinan en timeouts impredecibles.
"""

import logging

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from framework import config

Locator = tuple[str, str]


class BasePage:
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, config.timeout())
        self.log = logging.getLogger(type(self).__name__)

    def step(self, description: str) -> None:
        """Registra un paso de negocio; los logs capturados se muestran por test en el reporte HTML."""
        self.log.info(description)

    def visible(self, locator: Locator) -> WebElement:
        return self.wait.until(ec.visibility_of_element_located(locator))

    def all_visible(self, locator: Locator) -> list[WebElement]:
        return self.wait.until(ec.visibility_of_all_elements_located(locator))

    def click(self, locator: Locator) -> None:
        self.wait.until(ec.element_to_be_clickable(locator)).click()

    def type(self, locator: Locator, text: str) -> None:
        element = self.visible(locator)
        element.clear()
        element.send_keys(text)

    def text_of(self, locator: Locator) -> str:
        return self.visible(locator).text.strip()

    def texts_of(self, locator: Locator) -> list[str]:
        return [element.text.strip() for element in self.all_visible(locator)]

    def is_present(self, locator: Locator) -> bool:
        """Comprobación sin espera, para elementos que pueden no estar presentes legítimamente."""
        return len(self.driver.find_elements(*locator)) > 0

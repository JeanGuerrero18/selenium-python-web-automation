"""Construye instancias locales de WebDriver.

Selenium Manager (incluido en Selenium 4) resuelve los binarios del driver,
así que no hace falta el paquete webdriver-manager ni un chromedriver manual.
"""

from selenium import webdriver
from selenium.webdriver.chromium.options import ChromiumOptions
from selenium.webdriver.remote.webdriver import WebDriver

from framework import config
from framework.browser import Browser


def create_driver(browser: Browser, headless: bool) -> WebDriver:
    if browser is Browser.CHROME:
        return webdriver.Chrome(options=_chromium_options(webdriver.ChromeOptions(), headless))
    if browser is Browser.EDGE:
        return webdriver.Edge(options=_chromium_options(webdriver.EdgeOptions(), headless))
    return webdriver.Firefox(options=_firefox_options(headless))


def _chromium_options(options: ChromiumOptions, headless: bool) -> ChromiumOptions:
    if headless:
        options.add_argument("--headless=new")
    options.add_argument(f"--window-size={_width()},{_height()}")
    # Desactiva el gestor de contraseñas y los avisos de contraseñas filtradas: sus popups nativos
    # aparecen tras el login en los sitios demo y pueden quitarle el foco a la página.
    options.add_experimental_option(
        "prefs",
        {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False,
        },
    )
    return options


def _firefox_options(headless: bool) -> webdriver.FirefoxOptions:
    options = webdriver.FirefoxOptions()
    if headless:
        options.add_argument("-headless")
    options.add_argument(f"--width={_width()}")
    options.add_argument(f"--height={_height()}")
    return options


def _width() -> int:
    return config.get_int("window.width")


def _height() -> int:
    return config.get_int("window.height")

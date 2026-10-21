import pytest

from data import saucedemo
from pages.saucedemo.inventory_page import InventoryPage
from pages.saucedemo.login_page import LoginPage


@pytest.fixture
def login_page(driver) -> LoginPage:
    return LoginPage(driver).open()


@pytest.fixture
def inventory(login_page) -> InventoryPage:
    """Página del catálogo, con sesión ya iniciada como el usuario estándar."""
    return login_page.login_as(saucedemo.STANDARD_USER, saucedemo.password())

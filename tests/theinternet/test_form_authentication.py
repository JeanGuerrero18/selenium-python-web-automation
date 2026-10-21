import pytest

from framework import config
from pages.theinternet.form_authentication_page import FormAuthenticationPage

pytestmark = pytest.mark.regression


def _valid_username() -> str:
    return config.get("theinternet.username")


def _valid_password() -> str:
    return config.get("theinternet.password")


@pytest.mark.smoke
def test_valid_login_opens_secure_area(driver):
    """Las credenciales válidas abren el área segura"""
    page = FormAuthenticationPage(driver).open().login(_valid_username(), _valid_password())

    assert page.flash_message() == "You logged into a secure area!"
    assert page.header() == "Secure Area"


@pytest.mark.parametrize(
    ("username", "password", "expected_message"),
    [
        pytest.param("unknown_user", None, "Your username is invalid!", id="unknown-username"),
        pytest.param(None, "wrong_password", "Your password is invalid!", id="wrong-password"),
    ],
)
def test_invalid_login_shows_error(driver, username, password, expected_message):
    """Las credenciales inválidas muestran el mensaje flash correspondiente"""
    # None significa "usar el valor válido"; se resuelve en ejecución para que apliquen los valores
    # sobrescritos.
    page = (
        FormAuthenticationPage(driver)
        .open()
        .login(username or _valid_username(), password or _valid_password())
    )

    assert page.flash_message() == expected_message

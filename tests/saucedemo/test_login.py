import pytest

from data import saucedemo

pytestmark = pytest.mark.regression


@pytest.mark.smoke
def test_valid_login_shows_inventory(inventory):
    """El usuario estándar llega al catálogo de productos"""
    assert inventory.title() == "Products"
    assert len(inventory.product_names()) == 6


def test_locked_out_user_sees_error(login_page):
    """El usuario bloqueado es rechazado con un mensaje específico"""
    login_page.attempt_login(saucedemo.LOCKED_OUT_USER, saucedemo.password())

    assert login_page.error_message() == "Epic sadface: Sorry, this user has been locked out."


@pytest.mark.parametrize(
    ("username", "password", "expected_error"),
    [
        pytest.param("", "any", "Epic sadface: Username is required", id="empty-username"),
        pytest.param(saucedemo.STANDARD_USER, "", "Epic sadface: Password is required", id="empty-password"),
        pytest.param(
            saucedemo.STANDARD_USER,
            "wrong_password",
            "Epic sadface: Username and password do not match any user in this service",
            id="wrong-password",
        ),
    ],
)
def test_invalid_login_shows_error(login_page, username, password, expected_error):
    """Las credenciales inválidas muestran el mensaje de validación correspondiente"""
    login_page.attempt_login(username, password)

    assert login_page.error_message() == expected_error


def test_logout_returns_to_login_page(inventory):
    """Cerrar sesión devuelve al usuario a la página de login"""
    login_page = inventory.header.logout()

    assert login_page.is_displayed()

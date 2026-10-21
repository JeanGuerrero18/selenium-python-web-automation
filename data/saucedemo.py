"""Datos de prueba de SauceDemo: cuentas de prueba publicadas, nombres del catálogo y un cliente."""

from dataclasses import dataclass

from framework import config

STANDARD_USER = "standard_user"
LOCKED_OUT_USER = "locked_out_user"

BACKPACK = "Sauce Labs Backpack"
BIKE_LIGHT = "Sauce Labs Bike Light"
BOLT_TSHIRT = "Sauce Labs Bolt T-Shirt"


def password() -> str:
    """Todas las cuentas de prueba de SauceDemo comparten la misma contraseña."""
    return config.get("saucedemo.password")


@dataclass(frozen=True)
class Customer:
    first_name: str
    last_name: str
    postal_code: str


VALID_CUSTOMER = Customer("Usuario", "A", "10001")

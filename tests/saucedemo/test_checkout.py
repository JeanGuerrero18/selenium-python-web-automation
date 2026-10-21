import pytest

from data.saucedemo import BACKPACK, BOLT_TSHIRT, VALID_CUSTOMER, Customer

pytestmark = pytest.mark.regression


@pytest.mark.smoke
def test_complete_purchase_end_to_end(inventory):
    """Compra de punta a punta, desde el login hasta la confirmación del pedido"""
    complete = (
        inventory.add_to_cart(BACKPACK).header.open_cart().checkout().continue_with(VALID_CUSTOMER).finish()
    )

    assert complete.confirmation_message() == "Thank you for your order!"


def test_overview_totals_are_consistent(inventory):
    """El resumen del pedido cuadra: subtotal de artículos y total con impuestos"""
    overview = (
        inventory.add_to_cart(BACKPACK)
        .add_to_cart(BOLT_TSHIRT)
        .header.open_cart()
        .checkout()
        .continue_with(VALID_CUSTOMER)
    )

    assert overview.subtotal() == sum(overview.item_prices())
    assert overview.total() == overview.subtotal() + overview.tax()


def test_checkout_requires_first_name(inventory):
    """El checkout no puede continuar sin el nombre"""
    information = (
        inventory.add_to_cart(BACKPACK)
        .header.open_cart()
        .checkout()
        .attempt_continue_with(Customer("", "A", "10001"))
    )

    assert information.error_message() == "Error: First Name is required"

import pytest

from data.saucedemo import BACKPACK, BIKE_LIGHT

pytestmark = pytest.mark.regression


@pytest.mark.smoke
def test_added_items_appear_in_cart(inventory):
    """Los productos agregados aparecen en el badge y en el carrito"""
    inventory.add_to_cart(BACKPACK).add_to_cart(BIKE_LIGHT)

    assert inventory.header.cart_count() == 2
    assert sorted(inventory.header.open_cart().item_names()) == sorted([BACKPACK, BIKE_LIGHT])


def test_removed_item_leaves_cart(inventory):
    """Quitar un producto actualiza el badge y el carrito"""
    inventory.add_to_cart(BACKPACK).add_to_cart(BIKE_LIGHT).remove_from_cart(BACKPACK)

    assert inventory.header.cart_count() == 1
    assert inventory.header.open_cart().item_names() == [BIKE_LIGHT]

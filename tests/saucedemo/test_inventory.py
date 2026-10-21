import pytest

from pages.saucedemo.inventory_page import SortOption

pytestmark = pytest.mark.regression


def test_sort_by_price_low_to_high(inventory):
    """Ordenar por precio de menor a mayor ordena el catálogo de forma ascendente"""
    prices = inventory.sort_by(SortOption.PRICE_LOW_TO_HIGH).product_prices()

    assert prices == sorted(prices)


def test_sort_by_name_z_to_a(inventory):
    """Ordenar por nombre de Z a A ordena el catálogo de forma descendente"""
    names = inventory.sort_by(SortOption.NAME_Z_TO_A).product_names()

    assert names == sorted(names, reverse=True)

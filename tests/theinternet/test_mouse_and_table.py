import pytest

from pages.theinternet.mouse_and_table_pages import HoversPage, SortableTablesPage

pytestmark = pytest.mark.regression


def test_hover_reveals_caption(driver):
    """Pasar el cursor sobre un avatar muestra su texto"""
    assert HoversPage(driver).open().caption_after_hover(0) == "name: user1"


def test_table_cell_is_found_by_row_and_column(driver):
    """Una celda se encuentra por la clave de fila y el encabezado de columna"""
    table = SortableTablesPage(driver).open()

    assert table.cell("Last Name", "Bach", "Due") == "$51.00"


def test_table_sorts_by_last_name(driver):
    """Hacer clic en un encabezado ordena la columna de forma ascendente"""
    last_names = SortableTablesPage(driver).open().sort_by("Last Name").column("Last Name")

    assert last_names == sorted(last_names)

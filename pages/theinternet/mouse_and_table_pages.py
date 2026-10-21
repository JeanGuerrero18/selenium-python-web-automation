from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec

from pages.theinternet.the_internet_page import TheInternetPage


class HoversPage(TheInternetPage):
    FIGURE = (By.CLASS_NAME, "figure")
    CAPTION_TITLE = (By.CSS_SELECTOR, ".figcaption h5")

    def open(self) -> "HoversPage":
        self.open_path("/hovers")
        return self

    def caption_after_hover(self, index: int) -> str:
        """Pasa el cursor sobre el avatar en ``index`` (base 0) y devuelve el texto que aparece."""
        self.step(f"Hover over avatar {index + 1}")
        figure = self.all_visible(self.FIGURE)[index]
        ActionChains(self.driver).move_to_element(figure).perform()
        caption = figure.find_element(*self.CAPTION_TITLE)
        return self.wait.until(ec.visibility_of(caption)).text.strip()


class SortableTablesPage(TheInternetPage):
    """Tabla del ejemplo 1 (sin clases útiles): las celdas se ubican por la posición del encabezado."""

    HEADERS = (By.CSS_SELECTOR, "#table1 thead th")
    ROWS = (By.CSS_SELECTOR, "#table1 tbody tr")
    CELLS = (By.TAG_NAME, "td")

    def open(self) -> "SortableTablesPage":
        self.open_path("/tables")
        return self

    def sort_by(self, header: str) -> "SortableTablesPage":
        self.step(f"Sort table by '{header}'")
        self.all_visible(self.HEADERS)[self._column_index(header)].click()
        return self

    def column(self, header: str) -> list[str]:
        index = self._column_index(header)
        return [row.find_elements(*self.CELLS)[index].text.strip() for row in self.all_visible(self.ROWS)]

    def cell(self, key_header: str, key_value: str, header: str) -> str:
        """Valor de ``header`` en la fila cuyo ``key_header`` es igual a ``key_value``."""
        key_index = self._column_index(key_header)
        value_index = self._column_index(header)
        for row in self.all_visible(self.ROWS):
            cells = row.find_elements(*self.CELLS)
            if cells[key_index].text.strip() == key_value:
                return cells[value_index].text.strip()
        raise NoSuchElementException(f"No row with {key_header} = {key_value}")

    def _column_index(self, header: str) -> int:
        for index, element in enumerate(self.all_visible(self.HEADERS)):
            if element.text.strip() == header:
                return index
        raise NoSuchElementException(f"No column named '{header}'")

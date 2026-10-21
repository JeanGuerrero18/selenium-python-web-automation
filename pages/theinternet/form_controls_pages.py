from pathlib import Path

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from pages.theinternet.the_internet_page import TheInternetPage


class CheckboxesPage(TheInternetPage):
    CHECKBOX = (By.CSS_SELECTOR, "#checkboxes input[type='checkbox']")

    def open(self) -> "CheckboxesPage":
        self.open_path("/checkboxes")
        return self

    def set_checked(self, index: int, checked: bool) -> "CheckboxesPage":
        """Garantiza que el checkbox en ``index`` (base 0) quede en el estado pedido."""
        self.step(f"{'Check' if checked else 'Uncheck'} checkbox {index + 1}")
        checkbox = self.all_visible(self.CHECKBOX)[index]
        if checkbox.is_selected() != checked:
            checkbox.click()
        return self

    def states(self) -> list[bool]:
        return [checkbox.is_selected() for checkbox in self.all_visible(self.CHECKBOX)]


class DropdownPage(TheInternetPage):
    DROPDOWN = (By.ID, "dropdown")

    def open(self) -> "DropdownPage":
        self.open_path("/dropdown")
        return self

    def select(self, visible_text: str) -> "DropdownPage":
        self.step(f"Select '{visible_text}'")
        self._dropdown().select_by_visible_text(visible_text)
        return self

    def selected_option(self) -> str:
        return self._dropdown().first_selected_option.text.strip()

    def _dropdown(self) -> Select:
        return Select(self.visible(self.DROPDOWN))


class FileUploadPage(TheInternetPage):
    FILE_INPUT = (By.ID, "file-upload")
    SUBMIT = (By.ID, "file-submit")
    UPLOADED_FILES = (By.ID, "uploaded-files")

    def open(self) -> "FileUploadPage":
        self.open_path("/upload")
        return self

    def upload(self, file: Path) -> "FileUploadPage":
        """Envía la ruta directamente al input de archivo; no interviene ningún diálogo nativo del SO."""
        self.step(f"Upload {file.name}")
        self.driver.find_element(*self.FILE_INPUT).send_keys(str(file.resolve()))
        self.click(self.SUBMIT)
        return self

    def uploaded_file_name(self) -> str:
        return self.text_of(self.UPLOADED_FILES)

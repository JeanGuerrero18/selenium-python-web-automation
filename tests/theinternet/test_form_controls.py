from pathlib import Path

import pytest

from pages.theinternet.form_controls_pages import CheckboxesPage, DropdownPage, FileUploadPage

pytestmark = pytest.mark.regression

SAMPLE_FILE = Path(__file__).resolve().parents[2] / "data" / "files" / "sample-upload.txt"


def test_checkboxes_can_be_toggled(driver):
    """Los checkboxes se pueden poner en un estado explícito"""
    page = CheckboxesPage(driver).open().set_checked(0, True).set_checked(1, False)

    assert page.states() == [True, False]


def test_dropdown_selects_option(driver):
    """El dropdown conserva la opción seleccionada"""
    page = DropdownPage(driver).open().select("Option 2")

    assert page.selected_option() == "Option 2"


def test_file_is_uploaded(driver):
    """Se sube un archivo de la carpeta data"""
    page = FileUploadPage(driver).open().upload(SAMPLE_FILE)

    assert page.uploaded_file_name() == "sample-upload.txt"

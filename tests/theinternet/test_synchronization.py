import pytest

from pages.theinternet.dynamic_loading_page import DynamicLoadingPage

pytestmark = pytest.mark.regression


@pytest.mark.smoke
def test_dynamically_loaded_element_appears(driver):
    """La espera explícita maneja contenido que se renderiza con retraso"""
    page = DynamicLoadingPage(driver).open().start()

    assert page.loaded_text() == "Hello World!"

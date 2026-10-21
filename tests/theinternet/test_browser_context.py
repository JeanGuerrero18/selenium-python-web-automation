import pytest

from pages.theinternet.browser_context_pages import (
    JavaScriptAlertsPage,
    MultipleWindowsPage,
    NestedFramesPage,
)

pytestmark = pytest.mark.regression


def test_alert_is_accepted(driver):
    """La alerta JS se acepta"""
    page = JavaScriptAlertsPage(driver).open().accept_alert()

    assert page.result() == "You successfully clicked an alert"


def test_confirm_is_dismissed(driver):
    """El confirm JS se cancela"""
    page = JavaScriptAlertsPage(driver).open().dismiss_confirm()

    assert page.result() == "You clicked: Cancel"


def test_prompt_receives_text(driver):
    """El prompt JS recibe el texto escrito"""
    page = JavaScriptAlertsPage(driver).open().answer_prompt("Usuario A")

    assert page.result() == "You entered: Usuario A"


def test_new_window_is_opened_and_focused(driver):
    """El enlace abre una segunda ventana a la que el driver puede cambiar"""
    page = MultipleWindowsPage(driver).open().open_new_window()

    assert page.window_count() == 2
    assert page.heading() == "New Window"


def test_nested_frames_are_readable(driver):
    """El contenido de los frames anidados es accesible"""
    page = NestedFramesPage(driver).open()

    assert page.text_of_top_frame("frame-middle") == "MIDDLE"
    assert page.text_of_top_frame("frame-left") == "LEFT"
    assert page.text_of_bottom_frame() == "BOTTOM"

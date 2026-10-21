"""Alertas, ventanas y frames: todo lo que necesita driver.switch_to."""

from selenium.common.exceptions import NoSuchElementException, NoSuchFrameException
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from framework import config
from pages.theinternet.the_internet_page import TheInternetPage


class JavaScriptAlertsPage(TheInternetPage):
    ALERT_BUTTON = (By.CSS_SELECTOR, "button[onclick='jsAlert()']")
    CONFIRM_BUTTON = (By.CSS_SELECTOR, "button[onclick='jsConfirm()']")
    PROMPT_BUTTON = (By.CSS_SELECTOR, "button[onclick='jsPrompt()']")
    RESULT = (By.ID, "result")

    def open(self) -> "JavaScriptAlertsPage":
        self.open_path("/javascript_alerts")
        return self

    def accept_alert(self) -> "JavaScriptAlertsPage":
        self.step("Open JS alert and accept it")
        self.click(self.ALERT_BUTTON)
        self._wait_for_alert().accept()
        return self

    def dismiss_confirm(self) -> "JavaScriptAlertsPage":
        self.step("Open JS confirm and dismiss it")
        self.click(self.CONFIRM_BUTTON)
        self._wait_for_alert().dismiss()
        return self

    def answer_prompt(self, text: str) -> "JavaScriptAlertsPage":
        self.step(f"Open JS prompt and answer '{text}'")
        self.click(self.PROMPT_BUTTON)
        prompt = self._wait_for_alert()
        prompt.send_keys(text)
        prompt.accept()
        return self

    def result(self) -> str:
        return self.text_of(self.RESULT)

    def _wait_for_alert(self) -> Alert:
        return self.wait.until(ec.alert_is_present())


class MultipleWindowsPage(TheInternetPage):
    NEW_WINDOW_LINK = (By.CSS_SELECTOR, "a[href='/windows/new']")
    HEADING = (By.TAG_NAME, "h3")

    def open(self) -> "MultipleWindowsPage":
        self.open_path("/windows")
        return self

    def open_new_window(self) -> "MultipleWindowsPage":
        """Abre el enlace en una ventana nueva y cambia el driver a ella."""
        self.step("Open link in a new window and switch to it")
        original = self.driver.current_window_handle
        self.click(self.NEW_WINDOW_LINK)
        self.wait.until(ec.number_of_windows_to_be(2))
        new_handle = next(handle for handle in self.driver.window_handles if handle != original)
        self.driver.switch_to.window(new_handle)
        return self

    def heading(self) -> str:
        return self.text_of(self.HEADING)

    def window_count(self) -> int:
        return len(self.driver.window_handles)


class NestedFramesPage(TheInternetPage):
    BODY = (By.TAG_NAME, "body")

    def open(self) -> "NestedFramesPage":
        self.open_path("/nested_frames")
        return self

    def text_of_top_frame(self, child_frame_name: str) -> str:
        return self._text_of_frame("frame-top", child_frame_name)

    def text_of_bottom_frame(self) -> str:
        return self._text_of_frame("frame-bottom")

    def _text_of_frame(self, *frame_path: str) -> str:
        """Recorre toda la ruta de frames desde el documento principal en cada reintento.

        Cambiar de nivel en nivel puede dejar el driver dentro de un frame padre cuyo documento aún
        se está reemplazando mientras carga el frameset (se veía como un fallo intermitente en paralelo).
        """
        self.step(f"Read text of frame {' > '.join(frame_path)}")

        def read(driver):
            driver.switch_to.default_content()
            for frame in frame_path:
                driver.switch_to.frame(frame)
            return driver.find_element(*self.BODY).text.strip() or False

        try:
            return WebDriverWait(
                self.driver,
                config.timeout(),
                ignored_exceptions=(NoSuchFrameException, NoSuchElementException),
            ).until(read)
        finally:
            self.driver.switch_to.default_content()

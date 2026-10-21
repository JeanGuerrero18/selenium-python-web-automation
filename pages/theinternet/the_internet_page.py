from framework import config
from framework.base_page import BasePage


class TheInternetPage(BasePage):
    """Base de los ejemplos de The Internet: cada página vive en su propia ruta bajo un mismo host."""

    def open_path(self, path: str) -> None:
        self.step(f"Open {path}")
        self.driver.get(config.get("theinternet.url") + path)

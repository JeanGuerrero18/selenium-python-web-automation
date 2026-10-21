"""Fixtures compartidas y hooks de reporte de pytest-html."""

import html
import logging
import platform

import pytest
import pytest_html
from pytest_metadata.plugin import metadata_key
from selenium.common.exceptions import WebDriverException

from framework import config as settings
from framework.driver_factory import create_driver

log = logging.getLogger("conftest")


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption("--browser", default=None, help="chrome | firefox | edge (default: config.ini)")
    parser.addoption("--headless", action="store_true", default=None, help="run without a browser window")


def pytest_configure(config: pytest.Config) -> None:
    # Corre en el controlador y en cada worker de xdist, así todos ven los mismos valores sobrescritos.
    if config.getoption("browser"):
        settings.set_override("browser", config.getoption("browser"))
    if config.getoption("headless"):
        settings.set_override("headless", "true")

    metadata = config.stash[metadata_key]
    metadata["Browser"] = settings.browser().value
    metadata["Headless"] = str(settings.headless())
    metadata["OS"] = platform.platform()


@pytest.fixture
def driver():
    """Un navegador nuevo por test, para que los tests sean independientes y puedan correr en paralelo."""
    web_driver = create_driver(settings.browser(), settings.headless())
    yield web_driver
    web_driver.quit()


@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    report = yield
    report.description = (getattr(getattr(item, "function", None), "__doc__", None) or "").strip()
    if report.when == "call" and report.failed:
        _attach_screenshot(item, report)
    return report


def _attach_screenshot(item: pytest.Item, report: pytest.TestReport) -> None:
    web_driver = item.funcargs.get("driver")
    if web_driver is None:
        return
    try:
        screenshot = web_driver.get_screenshot_as_base64()
    except WebDriverException as error:
        # Un navegador caído no debe ocultar el fallo original.
        log.warning("Could not capture screenshot: %s", error.msg)
        return
    extras = getattr(report, "extras", [])
    extras.append(pytest_html.extras.png(screenshot, "Screenshot at failure"))
    report.extras = extras


def pytest_html_report_title(report) -> None:
    report.title = "Web Automation Report - SauceDemo & The Internet"


def pytest_html_results_table_header(cells: list[str]) -> None:
    cells.insert(2, "<th>Description</th>")


def pytest_html_results_table_row(report: pytest.TestReport, cells: list[str]) -> None:
    cells.insert(2, f"<td>{html.escape(getattr(report, 'description', ''))}</td>")

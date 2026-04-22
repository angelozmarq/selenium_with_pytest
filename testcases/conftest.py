from datetime import datetime
import os
from typing import Any, Iterator
import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from pytest_html import extras
from pytest_metadata.plugin import metadata_key


@pytest.fixture(scope="session", autouse=True)
def load_environment():
    load_dotenv(".env")


def pytest_addoption(parser: pytest.Parser):
    parser.addoption(
        "--browser", default="chrome", choices=["chrome", "firefox", "edge"], help="Select a browser for the test run."
    )
    parser.addoption("--headless", action="store_true", help="Determine if the test should run headless.")


@pytest.fixture(scope="class")
def driver(request: pytest.FixtureRequest) -> Iterator[WebDriver]:
    browser = request.config.getoption("--browser")
    is_headless = request.config.getoption("--headless")

    BROWSER_BUILDERS = {
        "chrome": _build_chrome,
        "firefox": _build_firefox,
        "edge": _build_edge,
    }

    driver = BROWSER_BUILDERS[browser](is_headless)
    driver.set_page_load_timeout(float(os.getenv("PAGE_LOAD_TIMEOUT", 30)))
    driver.maximize_window() if not is_headless else driver.set_window_size(1920, 1080)

    try:
        yield driver
    finally:
        driver.quit()


def _build_chrome(headless: bool) -> WebDriver:
    options = webdriver.ChromeOptions()
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
    }
    options.add_experimental_option("prefs", prefs)
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--disable-gpu")
    options.add_argument("--incognito")
    if headless:
        options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    return driver


def _build_firefox(headless: bool) -> WebDriver:
    options = webdriver.FirefoxOptions()
    options.add_argument("--disable-gpu")
    if headless:
        options.add_argument("-headless")
    driver = webdriver.Firefox(options=options)
    return driver


def _build_edge(headless: bool) -> WebDriver:
    options = webdriver.EdgeOptions()
    options.add_argument("--disable-gpu")
    if headless:
        options.add_argument("--headless")
    driver = webdriver.Edge(options=options)
    return driver


def pytest_configure(config: pytest.Config) -> None:
    if config.getoption("collectonly"):
        return

    reports_dir = os.path.join("reports", "html")
    os.makedirs(reports_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    html_option = config.getoption("--html")
    filename = f"{os.path.basename(f'{html_option}_{timestamp}')}.html" if html_option else f"report_{timestamp}.html"
    config.option.htmlpath = os.path.join(reports_dir, filename)

    if hasattr(config.option, "self_contained_html"):
        config.option.self_contained_html = True

    load_dotenv(".env")

    meta = config.stash[metadata_key]
    meta["Project"] = os.getenv("METADATA_PROJECT", "")
    meta["Server"] = os.getenv("METADATA_SERVER", "")
    meta["URL"] = os.getenv("METADATA_URL", "")
    for key in ["Packages", "Plugins", "JAVA_HOME"]:
        meta.pop(key, None)


def pytest_html_report_title(report: Any) -> None:
    report.title = "Selenium with Pytest Test Automation Report"


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            extra = getattr(report, "extras", [])
            extra.append(extras.image(driver.get_screenshot_as_base64()))
            report.extra = extra

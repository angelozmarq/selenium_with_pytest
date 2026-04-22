import os
import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from pages.login_page import LoginPage
from utilities.custom_logger import custom_logger

logger = custom_logger(__name__)


@pytest.fixture(autouse=True)
def goto_url(driver: WebDriver):
    URL = os.getenv("URL")
    driver.get(URL)
    yield
    driver.delete_all_cookies()


@pytest.mark.usefixtures("driver")
class TestLoginAccess:
    @pytest.mark.parametrize(
        "username, password, expected_url",
        [
            ("standard_user", "secret_sauce", "https://www.saucedemo.com/inventory.html"),
            ("locked_out_user", "secret_sauce", "https://www.saucedemo.com/"),
            ("problem_user", "secret_sauce", "https://www.saucedemo.com/inventory.html"),
            ("performance_glitch_user", "secret_sauce", "https://www.saucedemo.com/inventory.html"),
            ("error_user", "secret_sauce", "https://www.saucedemo.com/inventory.html"),
            ("visual_user", "secret_sauce", "https://www.saucedemo.com/inventory.html"),
        ],
        ids=[
            "standard_user",
            "locked_out_user",
            "problem_user",
            "performance_glitch_user",
            "error_user",
            "visual_user",
        ],
    )
    def test_login_access(self, driver: WebDriver, username, password, expected_url):
        lp = LoginPage(driver)
        lp.login(username, password)
        assert driver.current_url == expected_url


class TestLoginValidation:
    @pytest.mark.parametrize(
        "username, password, validation_msg",
        [
            ("standard_user", "", "Epic sadface: Password is required"),
            ("", "secret_sauce", "Epic sadface: Username is required"),
            ("standard_user", "wrongpass", "Epic sadface: Username and password do not match any user in this service"),
            (
                "wrongusername",
                "secret_sauce",
                "Epic sadface: Username and password do not match any user in this service",
            ),
            ("", "", "Epic sadface: Username is required"),
            ("locked_out_user", "secret_sauce", "Epic sadface: Sorry, this user has been locked out."),
        ],
        ids=[
            "Valid username and empty password.",
            "Empty username and valid password.",
            "Valid username and invalid password.",
            "Invalid username and valid password.",
            "Empty username and empty password.",
            "Locked out user.",
        ],
    )
    def test_login_validation(self, driver: WebDriver, username, password, validation_msg):
        lp = LoginPage(driver)
        lp.login(username, password)
        lp.base.wait_for_text(*lp.locator.ERROR_MSG, validation_msg)

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.base_page import BaseActions


class LoginPageLocators:
    INP_USERNAME = (By.ID, "user-name")
    INP_PASSWORD = (By.ID, "password")
    BTN_LOGIN = (By.ID, "login-button")
    ERROR_MSG = (By.CLASS_NAME, "error-message-container")


class LoginPage:
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.base = BaseActions(driver)
        self.locator = LoginPageLocators()

    def enter_username(self, username: str) -> None:
        self.base.fill(*self.locator.INP_USERNAME, username)

    def enter_password(self, password: str) -> None:
        self.base.fill(*self.locator.INP_PASSWORD, password)

    def click_login(self) -> None:
        self.base.click(*self.locator.BTN_LOGIN)

    def login(self, username: str, password: str) -> None:
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

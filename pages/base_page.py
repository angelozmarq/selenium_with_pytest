import os
from selenium.webdriver.common.by import ByType
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BaseActions:
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.timeout = float(os.getenv("DEFAULT_TIMEOUT"))
        self.wait = WebDriverWait(driver, timeout=self.timeout)

    def wait_for_visibility(self, by: ByType, locator: str):
        self.wait.until(
            EC.visibility_of_element_located((by, locator)),
            f"Element with locator [{by}, {locator}] is not visible within {self.timeout}s.",
        )

    def wait_for_text(self, by: ByType, locator: str, text: str):
        self.wait_for_visibility(by, locator)
        self.wait.until(
            EC.text_to_be_present_in_element((by, locator), text),
            f"Element with locator [{by}, {locator}] does not contain text [{text}] within {self.timeout}s.",
        )

    def wait_for_native_alert(self):
        self.wait.until(EC.alert_is_present(), "No native alerts are visible.")

    def find_element(self, by: ByType, locator: str) -> WebElement:
        return self.driver.find_element(by, locator)

    def click(self, by: ByType, locator: str) -> None:
        self.wait_for_visibility(by, locator)
        self.find_element(by, locator).click()

    def fill(self, by: ByType, locator: str, value: str | int) -> None:
        self.wait_for_visibility(by, locator)
        self.find_element(by, locator).send_keys(str(value))

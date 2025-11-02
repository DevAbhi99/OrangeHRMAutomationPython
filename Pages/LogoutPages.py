from Locators.LogoutLocators import LogoutLocator
from selenium.webdriver.common.by import By

class LogoutPages:
    def __init__(self, driver):
        self.driver=driver
        self.locator=LogoutLocator()

    def profileElement(self):
        return self.driver.find_element(By.XPATH, self.locator.profileXpath)

    def logoutElement(self):
        return self.driver.find_element(By.XPATH, self.locator.logoutBtnXpath)
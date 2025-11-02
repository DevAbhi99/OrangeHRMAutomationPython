from Locators.MainLocators import MainLocators
from selenium.webdriver.common.by import By

class MainPages:
    def __init__(self, driver):
        self.driver=driver
        self.locator=MainLocators()

    def adminElement(self):
        return self.driver.find_element(By.XPATH, self.locator.adminXpath)

    def jobElement(self):
        return self.driver.find_element(By.XPATH, self.locator.jobXpath)

    def jobTitlesElement(self):
        return self.driver.find_element(By.XPATH, self.locator.jobTitlesXpath)

        

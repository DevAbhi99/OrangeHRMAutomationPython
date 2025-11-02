from Locators.LoginLocators import LoginLocators
from selenium.webdriver.common.by import By

class LoginPages:
    def __init__(self, driver):
        self.driver=driver
        self.locator=LoginLocators()

    
    def usernameElement(self):
        return self.driver.find_element(By.XPATH, self.locator.usernameXpath)

    def passwordElement(self):
        return self.driver.find_element(By.XPATH, self.locator.passwordXpath)

    def loginBtnElement(self):
        return self.driver.find_element(By.XPATH, self.locator.loginBtnXpath)
from Pages.LogoutPages import LogoutPages

class LogoutController:
    def __init__(self, driver):
        self.driver=driver
        self.page=LogoutPages(self.driver)

    def profileClick(self):
        return self.page.profileElement().click()

    def logoutClick(self):
        return self.page.logoutElement().click()

from Pages.MainPages import MainPages

class MainController:
    def __init__(self, driver):
        self.driver=driver
        self.page=MainPages(self.driver)

    def adminClick(self):
        self.page.adminElement().click()

    def jobClick(self):
        self.page.jobElement().click()

    def jobTitlesClick(self):
        self.page.jobTitlesElement().click()

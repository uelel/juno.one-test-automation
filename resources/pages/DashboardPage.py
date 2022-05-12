from PageObjectLibrary import PageObject
from ProjectsPage import ProjectsPage

class DashboardPage(PageObject):

    PAGE_TITLE = "Dashboard - JunoPro"
    PAGE_URL = "https://testautomation.juno.one/#/dashboard"

    _locators = {
        "projects_button": "css=a[href='#/projects']",
        "burger_icon": "id=hamburger-container"
    }

    def click_projects_button(self):
        """
        Click Projects button on the left panel
        """
        try:
            self.selib.click_element(self.locator.projects_button)
        # Open left panel first
        except:
            self.selib.wait_until_element_is_visible(self.locator.burger_icon, timeout=10)
            self.selib.click_element(self.locator.burger_icon)
            self.selib.click_element(self.locator.projects_button)
        self.wait_until_page_loaded(url=ProjectsPage.PAGE_URL)
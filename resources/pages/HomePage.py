from PageObjectLibrary import PageObject
from SigninPage import SigninPage

class HomePage(PageObject):

    PAGE_TITLE = "Juno"

    PAGE_URL = "https://www.juno.one/"

    _locators = {
        "signin_button": "xpath=//a[text()='Sign in']"
    }

    def open_signin_page(self):
        """
        Click the Sign in button
        """
        self.selib.click_element(self.locator.signin_button)
        self.wait_until_page_loaded(url=SigninPage.PAGE_URL)
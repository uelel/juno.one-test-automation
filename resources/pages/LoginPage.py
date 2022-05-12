from PageObjectLibrary import PageObject
from DashboardPage import DashboardPage

from robot.libraries.BuiltIn import BuiltIn

class LoginPage(PageObject):

    PAGE_TITLE = "JunoPro"
    PAGE_URL = "https://testautomation.juno.one/#/login"

    _locators = {
        "email_field": "css=input[name=email]",
        "password_field": "css=input[name=password]",
        "signin_button": "css=button[data-cy='sign-in-button']"
    }

    def enter_email(self, email):
        self.selib.input_text(self.locator.email_field, email)

    def enter_password(self, password):
        self.selib.input_text(self.locator.password_field, password)

    def click_sign_in_button(self):
        self.selib.wait_until_element_is_visible(self.locator.signin_button)
        self.selib.click_element(self.locator.signin_button)
        self.wait_until_page_loaded(url=DashboardPage.PAGE_URL)
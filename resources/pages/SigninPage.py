from PageObjectLibrary import PageObject
from LoginPage import LoginPage

class SigninPage(PageObject):

    PAGE_TITLE = "JunoOne | SignIn"
    PAGE_URL = "https://www.juno.one/signIn"

    _locators = {
        "username_field": "css=form input.form_input",
        "gotologin_button": "css=a.login-button"
    }

    def enter_username(self, username):
        """
        Enter given username into field
        """
        self.selib.input_text(self.locator.username_field, username)

    def click_go_to_login_button(self):
        """
        Click Go To Login button
        """
        self.selib.click_element(self.locator.gotologin_button)
        self.wait_until_page_loaded(url=LoginPage.PAGE_URL)
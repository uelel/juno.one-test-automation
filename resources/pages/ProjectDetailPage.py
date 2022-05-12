import os
import requests

from PageObjectLibrary import PageObject

class ProjectDetailPage(PageObject):

    PAGE_TITLE = "JunoPro"
    PAGE_URL = "https://testautomation.juno.one/#/project"

    _locators = {
        "design_button": "css=a[href*='/design']",
        "new_design_field": "css=input[placeholder='+ Add Design']",
        "new_design_window": "css=.container",
        "table_rows": "css=table tbody tr",
        "message_success": "css=div.el-message--success",
        "loading_wheel": "css=div.loading-block",
        "design_desc_new": "xpath=//div[div[span[text()='+ Add description']]]",
        "design_desc_result": "css=.container div.markdown-body p",
        "design_comment_new": "xpath=//div[div[span[text()='+ Add first comment']]]",
        "design_comment_results": "css=.container table tbody tr",
        "markdown_editor": "css=div.wysiwyg-block",
        "markdown_textarea": "css=textarea[test-id=wysiwyg-text-area]",
        "markdown_save_button": "css=button[data-cy=wysiwyg-save-btn]",
        "markdown_attach_button": "css=button[data-cy=wysiwyg-attachment-btn]",
        "maxed_img": "css=img.viewer-move"
    }

    def _open_design_tab(self):
        """
        Open design tab on product page
        Wait until designs are fully loaded
        """
        self.selib.wait_until_element_is_visible(self.locator.design_button, timeout=10)
        self.selib.click_element(self.locator.design_button)
        self.wait_until_page_loaded(url=self.PAGE_URL)
        self.selib.wait_until_element_is_not_visible(self.locator.loading_wheel, timeout=10)

    def create_new_design(self, design_name):
        """
        Create new design with given name
        """
        # Open design tab
        self._open_design_tab()
        # Create unique design name
        design_name = self.create_unique_name(design_name)
        self.builtin.set_global_variable("${final design name}", design_name)
        # Enter design name into the field
        self.selib.wait_until_element_is_visible(self.locator.new_design_field, timeout=10)
        self.selib.input_text(self.locator.new_design_field, design_name)
        # Create new design
        self.selib.press_keys(self.locator.new_design_field, "ENTER")
        # Wait until created design appears in the table
        self.selib.wait_until_element_is_visible(self.locator.message_success, timeout=10)
        self.selib.wait_until_element_is_not_visible(self.locator.message_success, timeout=10)

    def open_design_with_name(self, design_name):
        """
        Find design with given name in design table
        Open window with given design
        @param{str} design_name
        """
        # Open design tab
        self._open_design_tab()
        # Find design in the table
        found = False
        design_name_els = self.selib.get_webelements(self.locator.table_rows + " td:nth-child(2) div")
        for el in design_name_els:
            if design_name in self.selib.get_text(el):
                self.selib.click_element(el)
                self.selib.wait_until_element_is_visible(self.locator.new_design_window, timeout=10)
                found = True
                break
        if not found:
            self.selib.wait_for_condition(
                "return false",
                timeout=0,
                error="No design with given name '%s' was found" % (design_name)
            )

    def created_design_should_be_displayed_in_the_table(self, design_name):
        """
        Check that design table contains first row with correct values
        """
        # Check design name
        self.selib.element_should_contain(
            self.locator.table_rows + ":first-child td:nth-child(2) div", design_name
        )

    def open_description_editor(self):
        """
        Open markdown editor within design description section
        """
        self.selib.wait_until_element_is_visible(self.locator.design_desc_new, timeout=10)
        self.selib.click_element(self.locator.design_desc_new)
        self.selib.wait_until_element_is_visible(self.locator.markdown_editor, timeout=10)

    def add_new_description(self, value):
        """
        Enter given value into markdown editor within design description section
        @param{str} value
        """
        # Enter description
        self.selib.input_text(self.locator.markdown_textarea, value)
        # Save description
        el = self.selib.get_webelement(self.locator.markdown_save_button)
        self.browser.execute_script("arguments[0].click();", el)
        # Wait until created design appears in the table
        self.selib.wait_until_element_is_visible(self.locator.message_success, timeout=10)
        self.selib.wait_until_element_is_not_visible(self.locator.message_success, timeout=10)

    def description_should_be_correctly_formatted(self, code):
        """
        Check that design description html is equal to given code
        @param{str} code - html code that should be markdown output
        """
        self.selib.element_attribute_value_should_be(
            self.locator.design_desc_result,
            "innerHTML",
            code,
            message="Formatting of markdown output is different from '%s'" % (code)
        )

    def open_comment_editor(self):
        """
        Open markdown editor within design comment section
        """
        self.selib.click_element(self.locator.design_comment_new)
        self.selib.wait_until_element_is_visible(self.locator.markdown_editor, timeout=10)

    def add_new_comment(self, value):
        """
        Enter given value into markdown editor within design comment section
        @param{str} value
        """
        # Enter comment
        self.selib.scroll_element_into_view(self.locator.markdown_textarea)
        self.selib.input_text(self.locator.markdown_textarea, value)
        # Save comment
        el = self.selib.get_webelement(self.locator.markdown_save_button)
        self.browser.execute_script("arguments[0].click();", el)
        # Wait until created design appears in the table
        self.selib.wait_until_element_is_visible(self.locator.message_success, timeout=10)
        self.selib.wait_until_element_is_not_visible(self.locator.message_success, timeout=10)

    def image_inside_comment_can_be_downloaded(self):
        """
        Check that image in last comment can be downloaded
        """
        # Maximize image within last comment
        last_comment_el = self.selib.get_webelement(
            self.locator.design_comment_results + ":last-child td:nth-child(2) div.view-block"
        )
        self.selib.click_element(last_comment_el)
        self.wait_until_page_loaded()
        img_url = self.selib.get_element_attribute(self.locator.maxed_img, "src")
        # Download image
        try:
            res = requests.get(img_url, allow_redirects=True)
            path = os.path.dirname(__file__).replace('/pages', '/download/image.jpg')
            open(path, 'wb').write(res.content)
        except Exception as ex:
            raise Exception("Comment image could not be downloaded.", ex)
from PageObjectLibrary import PageObject
from ProjectDetailPage import ProjectDetailPage

class ProjectsPage(PageObject):

    PAGE_TITLE = "Projects - Open - JunoPro"
    PAGE_URL = "https://testautomation.juno.one/#/projects"

    _locators = {
        "add_project_field": "css=input[placeholder='+ Add Project']",
        "description_field": "xpath=//textarea[preceding-sibling::label[text()='Short Description']]",
        "create_button": "xpath=//button[span[contains(text(), 'Create')]]",
        "new_project_window": "css=.container",
        "table_rows": "css=table tbody tr",
        "message_success": "css=div.el-message--success",
        "loading_wheel": "css=div.loading-block"
    }

    def open_projects_page(self):
        """
        Open projects page
        Wait until projects are fully loaded
        """
        self.selib.go_to(self.PAGE_URL)
        self.wait_until_page_loaded(url=self.PAGE_URL)
        self.selib.wait_until_element_is_not_visible(self.locator.loading_wheel, timeout=10)


    def open_new_project_window(self, project_name):
        """
        Open new project window
        Fill out project name
        """
        # Create unique project name
        project_name = self.create_unique_name(project_name)
        self.builtin.set_global_variable("${final project name}", project_name)
        # Enter project name into the field
        self.selib.input_text(self.locator.add_project_field, project_name)
        # Open project window
        self.selib.press_keys(self.locator.add_project_field, "ENTER")
        # Wait until project window appears
        self.selib.wait_until_element_is_visible(self.locator.description_field, timeout=10)

    def enter_project_description(self, description):
        """
        Enter project description into opened window
        """
        self.builtin.set_global_variable("${final project description}", description)
        self.selib.input_text(self.locator.description_field, description)
    
    def click_create_project_button(self):
        """
        Click create project button
        """
        self.selib.click_element(self.locator.create_button)
        self.wait_until_page_loaded()
        # Wait until created project appears in the table
        #self.selib.wait_until_element_is_not_visible(self.locator.new_project_window, timeout=10)
        self.selib.wait_until_element_is_visible(self.locator.message_success, timeout=10)
        self.selib.wait_until_element_is_not_visible(self.locator.message_success, timeout=10)

    def created_project_should_be_displayed_in_the_table(self, project_name, project_desc):
        """
        Check that project table contains first row with correct values
        """
        # Check project name
        self.selib.element_text_should_be(
            self.locator.table_rows + ":first-child td:nth-child(1)", project_name
        )
        # Check project description
        self.selib.element_text_should_be(
            self.locator.table_rows + ":first-child td:nth-child(2) div span", project_desc
        )

    def open_project_with_name(self, project_name):
        """
        Find project with given name in project table
        Open page with given project
        @param{str} project_name
        """
        found = False
        product_name_els = self.selib.get_webelements(self.locator.table_rows + " td:nth-child(1)")
        for el in product_name_els:
            if self.selib.get_text(el) == project_name:
                self.selib.click_element(el)
                self.wait_until_page_loaded(url=ProjectDetailPage.PAGE_URL)
                found = True
                break
        if not found:
            self.selib.wait_for_condition(
                "return false",
                timeout=0,
                error="No project with given name '%s' was found" % (project_name)
            )

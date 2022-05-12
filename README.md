# juno.one-test-automation

This is a Selenium/Robot Framework project automating few functionalities in juno.one platform.

## Description

Simple `Robot` test framework was created. Browser was controlled via `Python Selenium` interface with help of `robotframework-seleniumlibrary`. This library installs all necessary dependencies including `selenium` and `webdriver-manager` modules.

Testcase business logic was defined in `tests/testSuite.robot` file. I tried to make the business logic simple enough to keep testcases short and readable. Test data are stored in `test/testdata.py`.  

Page object files were created inside `resources/pages` folder that handle element recognition, page interactions and other operations specific to each webpage. `robotframework-pageobjectlibrary` was used for this purpose, even though I made slight changes so I decided to include the library inside `resources/PageObjectLibrary` for now. Test steps were implemented inside page object classes.  

Due of nature of testcases (login -> create project -> create entity -> test entity functions), `robotframework-dependencylibrary` was used to set dependencies between them.  

## Installation

1. Install [Robot Framework plugin](https://plugins.jenkins.io/robot/) to Jenkins.

2. Create new Jenkins job that pulls this repo and executes this shell script:

```
pip install robotframework robotframework-seleniumlibrary robotframework-dependencylibrary
robot -d ./results --pythonpath ./resources --pythonpath ./resources/pages tests/testSuite.robot
exit 0
```

## What would I improve when developing the project further

1. Test data are currently not cleaned - after each test run there are new project+design created. This would be  relatively easy (using Teardown keyword). It is very important to keep test environment lean.

2. Files are currently not directly uploaded, but a pre-uploaded URL is used. There are definitely some ways to interact with upload dialog in Robot framework.  

3. I can imagine that most functionalities reside on `ProjectDetailPage` page. For that reason, it would make sense to split this class into more subclasses (e.g. `Design`, `Issue`, `Test Case`).

4. I can also imagine some more sophisticated mapping of URLs in page objects (`PageObject.PAGE_URL`) so that relative URLs and regex patterns can be used.

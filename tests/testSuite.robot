*** Settings ***

Documentation     Test cases for basic functionality of juno.one platform

Library     SeleniumLibrary
Library     DependencyLibrary
Library     PageObjectLibrary

Library    HomePage
Library    SigninPage
Library    LoginPage
Library    DashboardPage
Library    ProjectsPage
Library    ProjectDetailPage

Variables    testdata.py

Suite Setup       Setup Browser
Suite Teardown    Teardown Browser

Test Teardown    Run Keyword If Test Failed    Capture Page Screenshot


*** Keywords ***

Setup Browser
    Open Browser    url=${url}    browser=headlesschrome
    Maximize Browser Window

Teardown browser
    Close Browser


*** Test Cases ***

Dashboard page should be visible after successful login
    [Setup]    Go To Page    HomePage
    Open Signin Page
    Enter Username    ${username}
    Click Go To Login Button
    Enter Email    ${email}
    Enter Password    ${password}
    Click Sign In Button
    The current page should be    DashboardPage


Created project should be visible in projects table
    Depends on test    Dashboard page should be visible after successful login
    [Setup]    Go To Page    DashboardPage
    Click Projects Button
    Open New Project Window    ${project name}
    Enter project description    ${project description}
    Click Create Project Button
    Created project should be displayed in the table    ${final project name}    ${final project description}


Created design should be visible in design table
    Depends on test    Dashboard page should be visible after successful login
    Depends on test    Created project should be visible in projects table
    [Setup]    Open Projects Page
    Open Project With Name    ${final project name}
    Create New Design    ${design name}
    Created design should be displayed in the table    ${final design name}


Markdown formatting inside design description is working correctly
    Depends on test    Dashboard page should be visible after successful login
    Depends on test    Created project should be visible in projects table
    Depends on test    Created design should be visible in design table
    [Setup]    Open Projects Page
    Open Project With Name    ${final project name}
    Open Design With Name    ${final design name}
    Open Description Editor
    Add New Description    ${design description input}
    Description should be correctly formatted    ${design description output}


It is possible to upload images inside design comments
    Depends on test    Dashboard page should be visible after successful login
    Depends on test    Created project should be visible in projects table
    Depends on test    Created design should be visible in design table
    [Setup]    Open Projects Page
    Open Project With Name    ${final project name}
    Open Design With Name    ${final design name}
    Open Comment Editor
    Add New Comment    ${design comment}
    Image inside comment can be downloaded
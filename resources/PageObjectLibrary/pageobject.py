from __future__ import absolute_import, unicode_literals

from abc import ABCMeta
import warnings

import robot.api
from robot.libraries.BuiltIn import BuiltIn

from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

import six
import random

from .locatormap import LocatorMap


class PageObject(six.with_metaclass(ABCMeta, object)):

    PAGE_URL = None
    PAGE_TITLE = None

    def __init__(self):
        self.logger = robot.api.logger
        self.locator = LocatorMap(getattr(self, "_locators", {}))
        self.builtin = BuiltIn()

    # N.B. selib, browser use @property so that a
    # subclass can be instantiated outside of the context of a running
    # test (eg: by libdoc, robotframework-hub, etc)
    @property
    def se2lib(self):
        warnings.warn("se2lib is deprecated. Use selib intead.", warnings.DeprecationWarning)
        return self.selib

    @property
    def selib(self):
        return self.builtin.get_library_instance("SeleniumLibrary")

    @property
    def browser(self):
        return self.selib.driver

    def __str__(self):
        return self.__class__.__name__

    def get_page_name(self):
        """Return the name of the current page """
        return self.__class__.__name__

    def wait_until_page_loaded(self, url=None, timeout=10):
        """
        Wait until page finished loading by checking document.readyState
        @param{str} url - if given, wait until it is contained in current url
        @param{int} timeout - wait timeout (default 10s)
        """
        if url:
            self.selib.wait_until_location_contains(url, timeout=timeout)
        self.selib.wait_for_condition("return (document.readyState == 'complete')", timeout=timeout)

    def create_unique_name(self, string):
        """
        Add random 3 digits to end of given string
        @param{str} string
        @return{str} edited string
        """
        seq = ''.join(str(x) for x in random.sample(range(1,9),3))
        return string + " " + seq

    def _is_current_page(self):
        """Determine if this page object represents the current page.

        This works by comparing the current page title to the class
        variable PAGE_TITLE.

        Unless their page titles are unique, page objects should
        override this function. For example, a common solution is to
        look at the url of the current page, or to look for a specific
        heading or element on the page.

        """

        actual_title = self.selib.get_title()
        expected_title = self.PAGE_TITLE

        if actual_title.lower() == expected_title.lower():
            return True

        self.logger.info("expected title: '%s'" % expected_title)
        self.logger.info("  actual title: '%s'" % actual_title)
        raise Exception("expected title to be '%s' but it was '%s'" % (expected_title, actual_title))
        return False
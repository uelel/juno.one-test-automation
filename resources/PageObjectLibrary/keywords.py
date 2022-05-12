"""PageObjectLibrary

A library to support the creation of page objects using
selenium and SeleniuimLibrary.

Note: The keywords in this file need to work even if there is no
current page object, which is why they are here instead of on the
PageObject model.

"""

from __future__ import print_function, absolute_import, unicode_literals
import six

import robot.api
from robot.libraries.BuiltIn import BuiltIn


from .pageobject import PageObject
try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

import re

class PageObjectLibraryKeywords(object):

    ROBOT_LIBRARY_SCOPE = "TEST SUITE"

    def __init__(self):
        self.builtin = BuiltIn()
        self.logger = robot.api.logger

    def the_current_page_should_be(self, page_name):
        """Fails if the name of the current page is not the given page name

        ``page_name`` is the name you would use to import the page.

        This keyword will import the given page object, put it at the
        front of the Robot library search order, then call the method
        ``_is_current_page`` on the library. The default
        implementation of this method will compare the page title to
        the ``PAGE_TITLE`` attribute of the page object, but this
        implementation can be overridden by each page object.

        """

        page = self._get_page_object(page_name)

        # This causes robot to automatically resolve keyword
        # conflicts by looking in the current page first.
        if page._is_current_page():
            # only way to get the current order is to set a
            # new order. Once done, if there actually was an
            # old order, preserve the old but make sure our
            # page is at the front of the list
            old_order = self.builtin.set_library_search_order()
            new_order = ([str(page)],) + old_order
            self.builtin.set_library_search_order(new_order)
            return

        # If we get here, we're not on the page we think we're on
        raise Exception("Expected page to be %s but it was not" % page_name)

    def go_to_page(self, page_name):
        """

        """
        page = self._get_page_object(page_name)
        #domain = self.builtin.get_variable_value("${DOMAIN}")
        #url = page_root if page_root is not None else page.selib.get_location()
        #(scheme, netloc, path, parameters, query, fragment) = urlparse(actual_url)
        #url = "%s://%s%s" % (scheme, netloc, page.PAGE_URL)
        page.selib.go_to(page.PAGE_URL)
        page.wait_until_page_loaded(url=page.PAGE_URL)

    def _get_page_object(self, page_name):
        """Import the page object if necessary, then return the handle to the library

        Note: If the page object has already been imported, it won't be imported again.
        """

        try:
            page = self.builtin.get_library_instance(page_name)

        except RuntimeError:
            self.builtin.import_library(page_name)
            page = self.builtin.get_library_instance(page_name)

        return page

    def get_to_page(self, page_name):
        """

        """
        page = self._get_page_object(page_name)
        #domain = self.builtin.get_variable_value("${DOMAIN}")
        actual_url = page.selib.get_location()
        #result = re.search(domain+page.PAGE_URL, actual_url)
        #self.builtin.log_to_console(result)

        # if actual_url.path belongs to page.PAGE_URL:
        # => already on page
        # if not:
        # Depends on test keyword

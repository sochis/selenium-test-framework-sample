#!/usr/bin/env python3
""" This is Util tests for element. """

import logging
import pytest

from lib.pom.google.google import Google

logger = logging.getLogger(__name__)


@pytest.mark.usefixtures("conftests_fixture", "testcase_fixture")
class TestPartnersSit:
    """
    Unit Test suite
    """

    # pylint: disable=no-member,too-many-statements
    @classmethod
    @pytest.fixture(scope="function")
    def testcase_fixture(cls):
        """
        Create Google Page Object Model.
        """
        logger.info("[test_init] Preparing the application tests")
        cls.google = Google(cls.driver)
        cls.home = cls.google.home
        yield
        logger.info("Test DONE")

    @pytest.mark.tc_element
    def test_element_functions(self):
        """ Unit test for Element class. """
        logger.info("Start test for element class.")
        self.home.open()
        self.home.search_box_input.get()
        self.home.search_box_input.get_elements()
        self.home.search_box_input.focus(prevent_scroll=False)
        self.home.search_box_input.send_keys("Search google")
        assert self.home.search_box_input.get_attribute("value") == "Search google"
        assert self.home.search_box_input.wait_for_text(expected_text="Search google", value_flag=True)
        self.home.search_box_input.is_displayed()
        self.home.google_search_submit.click()
        logger.info("Completed test for Element.")

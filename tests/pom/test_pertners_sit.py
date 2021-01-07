#!/usr/bin/env python3
""" This is Google search home POM tests. """

import logging
import pytest

from lib.pom.google.google import Google

logger = logging.getLogger(__name__)


@pytest.mark.usefixtures("conftests_fixture", "testcase_fixture")
class TestGoogle:
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

    @pytest.mark.tc_create_concept_page
    def test_create_concept_page(self):
        """ Unit test for searching anything on Google search page. """
        logger.info("Start test for searching anything on Google search page.")
        self.home.open()
        self.home.search_box_input.send_keys("search google")
        self.home.google_search_submit.click()
        logger.info("Completed test for searching anything on Google search page..")

#!/usr/bin/env python3
"""This is the page object of Google search Home page"""
import logging

from selenium.webdriver.common.by import By
from lib.base.base import Base
from lib.utils.common.web_element.decorator import elements
from lib.utils.common.web_element.element import Element

logger = logging.getLogger(__name__)

TEST_IDS = {
    'page_id': 'gsr',
    'search_box_input': ('//*[@name="q"]', By.XPATH),
    'google_search_submit': ('//*[@name="btnK"]', By.XPATH),
}


@elements(TEST_IDS)
class Home(Base):
    """
    POM class for Google Search Home
    """
    page_id: Element
    search_box_input: Element
    google_search_submit: Element

    def open(self, wait_time: int = 60) -> None:
        """ Open Google Search home page

        Arguments:
            wait_time(int): maximum wait time for display elements (default=60sec)
        Raises:
            TimeoutException: Failed to open page.
        """
        logger.info("Open Google Search Home page from URL.")
        self.driver.get('https://www.google.com/')
        self.page_id.get(max_wait=wait_time)

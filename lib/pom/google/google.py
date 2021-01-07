#!/usr/bin/env python3
"""top application module
Google search structure
"""
import logging

from selenium import webdriver
from .home import Home

logger = logging.getLogger(__name__)


class Google:
    """
    Application class for Google.
    """
    _link_count: int = 0

    def __init__(self, driver: webdriver):
        self.driver = driver

    # Represents the top application
    def open(self) -> None:
        """ Open the Google Top Page
        """
        logger.info("Open Google Top page from URL.")
        self.driver.get('https://www.google.com/')

    def close(self) -> None:
        """
        Closes the current browser.
        """
        self.driver.close()

    @property
    def home(self) -> Home:
        """ Create Google Search Home Page Object Model.
        """
        return Home(self.driver)

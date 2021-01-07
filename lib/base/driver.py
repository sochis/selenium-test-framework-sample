#!/usr/bin/env python3
""" Base of test class """

import logging
from selenium.webdriver import Remote, Chrome
from lib.utils.common.driver_setting import set_chrome_driver_options

logger = logging.getLogger(__name__)


def setup_chrome_driver_instances(headless: bool = True) -> Chrome:
    """ Setup webdriver

    Arguments:
        headless(bool): Show browser or not.

    Return:
        driver(Chrome): Chrome webdriver
    """
    driver = set_chrome_driver_options(headless)
    logger.info("Webdriver created.")

    return driver


def teardown_driver(driver: Remote) -> None:
    """Teardown webdriver

    Arguments:
        driver(Remote): Show browser or not.
    """
    driver.quit()
    logger.info("Webdriver closed.")

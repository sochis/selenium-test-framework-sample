#!/usr/bin/env python3
""" Base of test class """
# pylint: disable=unused-import

import logging
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

logger = logging.getLogger(__name__)


def set_chrome_driver_options(headless: bool = True) -> Chrome:
    """ Setup webdriver

    Arguments:
        headless(bool): Show browser or not.

    Return:
        driver(Chrome): Chrome webdriver
    """
    options = Options()
    options.binary_location = '/bin/google-chrome'
    if headless:
        options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument("--disable-application-cache")
    options.add_argument("--disable-infobars")
    options.add_argument("--hide-scrollbars")
    options.add_argument('--no-sandbox')
    options.add_argument("--enable-logging")
    options.add_argument("--log-level=2")
    options.add_argument("--ignore-certificate-errors")
    driver = Chrome(options=options)
    driver.maximize_window()

    return driver

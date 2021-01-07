#!/usr/bin/env python3
"""This is the command line tool for search on google"""
import argparse

from lib.base.driver import setup_chrome_driver_instances, teardown_driver
from lib.pom.google.google import Google
from lib.utils.common.logger_setting import get_logger

logger = get_logger()


def search_google(search_text: str, headless: bool) -> None:
    """ Open Create Concept page

    Arguments:
        search_text(str): Text for search on google.
        headless(bool): Show browser or not.
    """
    driver = setup_chrome_driver_instances(headless)
    try:
        google = Google(driver)

        logger.info("Start to set params to Create Concept Stap1.")
        home = google.home
        home.open()

        home.search_box_input.send_keys(search_text)
        home.google_search_submit.click()

    finally:
        teardown_driver(driver)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='commandline_tool.py',
        usage='Search anything on google from UI.',
        description='Add params needed for search.',
        epilog='end',
        add_help=True,
    )
    # Add arguments
    parser.add_argument('-s', '--search-text', help='*Required. Text for search on google', required=True)
    parser.add_argument('-hl', '--headless', help='*Required. Show browser or not.', action='store_true')

    # Analyse args
    args = parser.parse_args()

    # Execute ui operation by selenium.
    search_google(args.search_text, args.headless)

#!/usr/bin/env python3
""" For setup and teardown driver """
import logging
import pytest
from _pytest.fixtures import SubRequest
from lib.utils.common.driver_setting import set_chrome_driver_options

logger = logging.getLogger(__name__)


@pytest.fixture(scope='class', name='driver_fixture')  # type: ignore
def driver_fixture(request: SubRequest) -> None:
    """ session scope Fixture to create and quit driver.

    Args:
        request: a sub request for handling getting a fixture from a test function/fixture.
    Yields:
        None
    """
    request.cls.driver = set_chrome_driver_options()
    logger.info("Webdriver created.")

    yield

    request.cls.driver.quit()
    logger.info("Webdriver closed.")

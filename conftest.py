#!/usr/bin/env python3
""" Conftest file for pytest app testing """

import logging
import pytest
from tests.base.driver import *

logger = logging.getLogger(__name__)


@pytest.fixture(scope='class')
def conftests_fixture(driver_fixture):
    """
    fixture executed once per test suite. Should contain
    code common to all test suites in the project.
    """
    logger.debug("Conftest fixture - setting up the test suite")
    yield
    logger.debug("Conftest fixture - tearing down the test suite")

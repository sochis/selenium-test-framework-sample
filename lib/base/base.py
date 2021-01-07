#!/usr/bin/env python3
"""Base class"""

import logging
from selenium.webdriver import Remote

logger = logging.getLogger(__name__)


class Base:
    """
    Base class for POM.
    """
    def __init__(self, driver: Remote):
        self.driver = driver

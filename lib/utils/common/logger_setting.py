#!/usr/bin/env python3
""" Base of setting log """

import logging
import logging.config


def get_logger() -> logging.Logger:
    """ Setup logger
    """
    logging.config.fileConfig('logging.ini', disable_existing_loggers=False)
    logger = logging.getLogger(__name__)

    return logger

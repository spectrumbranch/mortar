"""
This module provides a logging facility.
"""

import logging
from logging import DEBUG, ERROR, INFO, WARNING, debug, error, info, warning

__all__ = ['debug', 'info', 'warning', 'error', 'DEBUG', 'INFO', 'WARNING',
           'ERROR']


def set_level(level: str) -> None:
    """ Set the log level for the root logger. """

    logging.getLogger('root').setLevel(level)

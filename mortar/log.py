"""
This module provides a logging facility.
"""

from logging import (debug, info, warning, error, DEBUG, INFO,
                     WARNING, ERROR)
import logging

__all__ = ['debug', 'info', 'warning', 'error', 'DEBUG', 'INFO', 'WARNING',
           'ERROR']


def set_level(level: str) -> None:
    """ Set the log level for the root logger. """

    logging.getLogger('root').setLevel(level)

from logging import (debug, info, warning, error, DEBUG, INFO,
                     WARNING, ERROR)
import logging

__all__ = ['debug', 'info', 'warning', 'error', 'DEBUG', 'INFO', 'WARNING',
           'ERROR']


def set_level(level: str) -> None:
    logging.getLogger('root').setLevel(level)

"""
mortar is a set of tools for evaluating OCR results for games.
"""

import os

__pdoc__ = {
    'examples': False
}


if os.name != 'posix':
    raise Exception('This package is only supported under WSL.')

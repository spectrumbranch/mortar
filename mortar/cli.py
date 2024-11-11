"""
This module provides an interactive shell interface to the mortar package.
"""

import sys

import IPython
from traitlets.config import Config

# The first command line argument, if provided, is the script to run.

_file = sys.argv[1] if len(sys.argv) != 1 else None


def main() -> int:
    """ This is the script's entry point. """

    c = Config()

    # On startup, make mortar facilities available in the IPython shell.

    c.InteractiveShellApp.exec_lines = [
        'from mortar.pipeline import *',
        'print("mortar command line interface")'
    ]

    c.InteractiveShell.confirm_exit = False
    c.TerminalIPythonApp.display_banner = False

    # If a script argument was provided, run it. Remain in the shell after the
    # script has completed.

    if _file is not None:
        c.InteractiveShellApp.file_to_run = _file

    c.TerminalIPythonApp.force_interact = True

    IPython.start_ipython(config=c)  # type: ignore[no-untyped-call]

    return 0

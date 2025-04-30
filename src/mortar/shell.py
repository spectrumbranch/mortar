"""
This module provides an interactive shell interface to the mortar package.
"""

import IPython
from traitlets.config import Config


def run(file: str | None) -> int:
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

    if file is not None:
        c.InteractiveShellApp.file_to_run = file

    c.TerminalIPythonApp.force_interact = True

    IPython.start_ipython(  # type: ignore[no-untyped-call] # pyright: ignore[reportUnknownMemberType] # noqa: E501
        config=c, argv=[]
    )

    return 0

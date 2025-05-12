"""
This module provides an interactive shell interface to the mortar package.
"""

from typing import cast

import IPython
from IPython.core.shellapp import InteractiveShellApp
from IPython.terminal.interactiveshell import TerminalInteractiveShell
from IPython.terminal.ipapp import TerminalIPythonApp
from traitlets.config import Config


def run(file: str | None) -> int:
    c = Config()

    # On startup, make mortar facilities available in the IPython shell.

    interactive_shell_app = cast(InteractiveShellApp, c.InteractiveShellApp)

    terminal_ipython_app = cast(TerminalIPythonApp, c.TerminalIPythonApp)

    interactive_shell_app.exec_lines = [
        'from mortar.pipeline import *',
        'print("mortar command line interface")'
    ]

    interactive_shell = cast(TerminalInteractiveShell, c.InteractiveShell)

    interactive_shell.confirm_exit = False

    terminal_ipython_app.display_banner = False

    # If a script argument was provided, run it. Remain in the shell after the
    # script has completed.

    if file is not None:
        interactive_shell_app.file_to_run = file

    terminal_ipython_app.force_interact = True

    IPython.start_ipython(  # type: ignore[no-untyped-call] # pyright: ignore[reportUnknownMemberType] # noqa: E501
        config=c, argv=[]
    )

    return 0

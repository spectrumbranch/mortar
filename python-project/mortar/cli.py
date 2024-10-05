import sys

import IPython
from traitlets.config import Config
# Make mortar facilities available in the IPython shell we'll embed on startup.

_file = sys.argv[1] if len(sys.argv) != 1 else None


def main() -> int:
    c = Config()
    c.InteractiveShellApp.exec_lines = [
        'from mortar.pipeline import *',
        'print("mortar command line interface")'
    ]

    c.InteractiveShell.confirm_exit = False
    c.TerminalIPythonApp.display_banner = False

    if _file is not None:
        c.InteractiveShellApp.file_to_run = _file

    c.TerminalIPythonApp.force_interact = True

    IPython.start_ipython(config=c)

    return 0

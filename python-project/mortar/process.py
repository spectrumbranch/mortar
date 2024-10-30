"""
This module provides facilities for executing operating system processes.
"""

import subprocess
from subprocess import CalledProcessError, CompletedProcess

import mortar.log as log


def run(*args, **kwargs) -> CompletedProcess:
    """
    Run the command described by args in a child process. args is a sequence
    representing the command name and its space-separated arguments.

    Capture and log stdout and stderr. Raise CalledProcessError if the child
    exits with a non-zero code.

    Return a CompletedProcess instance with the result.

    kwargs are passed through to the underlying call to subprocess.run.
    """

    log.info(f'run {args}')

    try:
        result = subprocess.run(
            *args, capture_output=True, check=True, **kwargs)
    except CalledProcessError as e:
        log.error(f'stdout={e.stdout}')
        log.error(f'stderr={e.stderr}')

        raise e

    log.info(f'stdout={result.stdout}')
    log.info(f'stderr={result.stderr}')

    return result

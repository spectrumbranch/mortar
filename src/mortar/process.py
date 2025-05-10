"""
This module provides facilities for executing operating system processes.
"""

import subprocess
from subprocess import CalledProcessError, CompletedProcess
from typing import Any, cast

from mktech import log

__all__ = ['CompletedProcess', 'run']


def run(
    *args: Any,  # pyright: ignore[reportAny,reportExplicitAny]
    **kwargs: Any,  # pyright: ignore[reportAny,reportExplicitAny]
) -> CompletedProcess[bytes]:
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
        result: CompletedProcess[bytes] = subprocess.run(  # pyright: ignore[reportUnknownVariableType] # noqa: E501
            *args, capture_output=True, check=True, **kwargs  # pyright: ignore[reportAny] # noqa: E501
        )
    except CalledProcessError as e:
        log.error(f'stdout={e.stdout}')  # pyright: ignore[reportAny]
        log.error(f'stderr={e.stderr}')  # pyright: ignore[reportAny]

        raise e

    log.info(f'stdout={cast(str, result.stdout)}')
    log.info(f'stderr={cast(str, result.stderr)}')

    return result  # pyright: ignore[reportUnknownVariableType]

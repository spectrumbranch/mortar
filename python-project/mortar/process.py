import subprocess
from subprocess import CalledProcessError, CompletedProcess

import mortar.log as log


def run(*args, **kwargs) -> CompletedProcess:
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

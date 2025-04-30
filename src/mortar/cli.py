import click
from mktech import log
from mktech.cli import from_config
from mktech.path import Path

import mortar.config
from mortar.config import Config

from . import shell, tesseract, video

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(
    context_settings=CONTEXT_SETTINGS,
    no_args_is_help=True,
)
@from_config(Config)
def cli(config: Config) -> None:
    mortar.config.set_config(config)

    log.init(config.log_level)


@cli.command('shell')
@click.argument('file', required=False)
def shell_command(file: str | None) -> None:
    """
    Start a mortar shell

    The optional FILE argument is a path to a Python file. If FILE is
    provided, the shell will run it after initialization.
    """

    if shell.run(file) != 0:
        raise click.ClickException('Command failed.')


@cli.command('tesseract')
@click.argument(
    'image', required=True, type=click.Path(dir_okay=False, path_type=Path)
)
def tesseract_command(image: Path) -> None:
    """
    Generate OCR text from an image using Tesseract, and print the OCR result.
    """

    tesseract.print_ocr(str(image))


@cli.command('video')
@click.argument('input', type=click.Path(file_okay=False, path_type=Path))
def video_command(input: Path) -> None:
    """
    Extract frames from all input videos in INPUT.
    """

    if video.extract_frames(input) != 0:
        raise click.ClickException('Command failed.')


def main() -> None:
    cli()

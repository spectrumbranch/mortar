import click
from mktech.path import Path

from . import shell, tesseract

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(
    context_settings=CONTEXT_SETTINGS,
    no_args_is_help=True,
)
def cli() -> None:
    pass


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





def main() -> None:
    cli()

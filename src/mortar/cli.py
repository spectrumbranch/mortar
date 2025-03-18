import click

from . import shell

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








def main() -> None:
    cli()

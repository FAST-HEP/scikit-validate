"""Print scikit-validate version"""
import click

from skvalidate import __version__


@click.command(help=__doc__)
@click.option('--plain', is_flag=True)
def cli(plain):
    if plain:
        click.echo(__version__)
    else:
        click.echo("scikit-validate version: {}".format(__version__))

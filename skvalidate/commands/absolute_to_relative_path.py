"""
Command that translates absolute paths to relative paths.

Meant to provide functionality of ``realpath`` for older platforms.
"""
import os

import click

@click.command(help=__doc__)
@click.argument('absolute_path', type=click.Path())
@click.option('--relative-to', default=os.getcwd(), type=click.Path())
def cli(absolute_path, relative_to):
    relative_path = os.path.relpath(absolute_path, relative_to)
    relative_path = os.path.normpath(relative_path)
    click.echo(relative_path)

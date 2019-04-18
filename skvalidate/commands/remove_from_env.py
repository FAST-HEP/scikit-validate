"""Removes a path from an ENV variable.

 :Usage:

 .. code-block:: bash

    sv_remove_from_env $PATH $TO_BE_REMOVED

returns ``$PATH`` without paths _starting_ with ``$TO_BE_REMOVED``

"""
import click


@click.command(help=__doc__)
@click.argument('current_path')
@click.argument('remove')
def cli(current_path, remove):
    if not remove:
        return

    new_path = []
    for path in current_path.split(':'):
        if path.startswith(remove):
            continue
        new_path.append(path)
    click.echo(':'.join(new_path), nl=False)

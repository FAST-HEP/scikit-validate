"""
Command for displaying the contents of a ROOT file
"""
from __future__ import print_function

import logging

import click
import uproot

logging.basicConfig(level=logging.INFO)


@click.command()
@click.argument('input-file', type=click.Path(exists=True))
@click.option('--tree')
def cli(input_file, tree):
    f = uproot.open(input_file)
    if not tree:
        for key in f.keys():
            print('>'*10, 'Tree =', key)
            f[key].show()
        return

    if tree not in f:
        logging.error('Could not find tree "{}"'.format(tree))
        logging.info('Available trees:')
        for key in f.keys():
            print(key)
        return
    tree = f[tree]
    tree.show()

from __future__ import print_function

import click
from plumbum import colors

from skvalidate.software.detect import get_software_version


@click.command(help=__doc__)
@click.argument('software', nargs=-1, required=True)
def cli(software):
    for s in software:
        print('>> Detecting version for:', s)
        try:
            version = get_software_version(s)
            print('>>>> Found {} version {}'.format(s, version))
        except KeyError as e:
            print(colors.red | str(e.message))

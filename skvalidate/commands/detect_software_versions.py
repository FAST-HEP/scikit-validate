from __future__ import print_function

import click
from plumbum import colors

from skvalidate.software.detect import get_software_version
from skvalidate.io import write_data_to_json


@click.command(help=__doc__)
@click.argument('software', nargs=-1, required=True)
@click.option('-o', '--output', default='software_versions.json', type=click.Path())
def cli(software, output):
    software_versions = {}
    for s in software:
        print('>> Detecting version for:', s)
        try:
            version = get_software_version(s)
            print('>>>> Found {} version {}'.format(s, version))
            software_versions[s] = version
        except KeyError as e:
            print(colors.red | str(e.message))
    if software_versions:
        write_data_to_json(software_versions, output)

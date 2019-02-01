from __future__ import print_function

import click
from plumbum import colors

from skvalidate.software.detect import get_software_version
from skvalidate.io import update_data_in_json


@click.command(help=__doc__)
@click.argument('software', nargs=-1, required=True)
@click.option('-o', '--output', default='software_versions.json', type=click.Path())
@click.option('-p', '--prefix', default='build', type=click.Path())
@click.option('-q', '--quiet', count=True)
def cli(software, output, prefix, quiet):
    software_versions = {}
    software_versions[prefix] = {}
    for s in software:
        if quiet < 1:
            print('>> Detecting version for:', s)
        try:
            version = get_software_version(s)
            if quiet < 1:
                print('>>>> Found {} version {}'.format(s, version))
            software_versions[prefix][s] = version
        except KeyError as e:
            if quiet < 2:
                print(colors.red | str(e.message))
    if software_versions[prefix]:
        update_data_in_json(software_versions, output)

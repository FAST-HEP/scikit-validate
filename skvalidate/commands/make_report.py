"""Make a report based on a YAML config."""

from __future__ import print_function

import click

from skvalidate.report import Report


@click.command(help=__doc__)
@click.argument('config', required=True, type=click.Path(exists=True))
@click.option('-o', '--output', default='report.md', type=click.Path())
def cli(config, output):
    print('>> Making report using config:', config)
    report = Report.from_yaml(config)
    report.write(output)
    print('>> Created report:', output)

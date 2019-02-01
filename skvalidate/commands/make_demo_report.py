from __future__ import print_function
import os

import click

from skvalidate import __skvalidate_root__
from skvalidate.report import Report

__demo_config__ = os.path.join(__skvalidate_root__, 'data', 'config', 'report', 'demo.yml')
__demo_output__ = os.path.join(os.getcwd(), 'demo_report.md')

@click.command(help=__doc__)
def cli():
    print('>> Making report using config:', __demo_config__)
    report = Report.from_yaml(__demo_config__)
    report.write(__demo_output__)
    print('>> Created report:', __demo_output__)

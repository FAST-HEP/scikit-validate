import os

import click

from skvalidate import __skvalidate_root__
from skvalidate.report import Report

__demo_config__ = os.path.join(__skvalidate_root__, 'config', 'demo.yml')
__demo_config__ = '/Users/phxlk/workspace/FAST/scikit-validate/config/report/demo.yml'

@click.command(help=__doc__)
def cli():
    print ('Using config:', __demo_config__)
    report = Report.from_yaml(__demo_config__)

    # print(report)
    report.write()

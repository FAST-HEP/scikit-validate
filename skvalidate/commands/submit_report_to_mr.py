"""Submit report as a comment to a merge request"""

import click

from skvalidate.report import add_report_to_merge_request

@click.command(help=__doc__)
@click.argument('input_files', type=click.Path(exists=True), nargs=-1)
def cli(input_files):
    add_report_to_merge_request(input_files)

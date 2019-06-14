"""Check formatting of C++ code using clang-format"""

from __future__ import print_function

import click
from git import Repo
import plumbum

def check_clang_format():
    pass

def get_files_to_check():
    pass

def format_files(files):
    pass

def create_patch(output_file):
    pass

@click.command(help=__doc__)
@click.option('-o', '--output', default='apply-formatting.patch', type=click.Path())
def cli(output):
    if not check_clang_format():
        click.echo("clang-format command not found")
    files_to_check = get_files_to_check()
    if files_to_check:
        format_files(files_to_check)
        create_patch(output)

    # curl ${CI_PROJECT_URL}/-/jobs/${CI_JOB_ID}/artifacts/raw/apply-formatting.patch | git am


    return -1

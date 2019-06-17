"""Check formatting of C++ code using clang-format"""

from __future__ import print_function
import fnmatch
import os
import sys

import click
from plumbum import local
from plumbum.commands.processes import CommandNotFound

from skvalidate.report.cpp_check_format import create_report
from skvalidate.report.cpp_check_format import TEMPLATE as cpp_check_template
from skvalidate.git import create_patch, get_changed_files
from skvalidate.report import add_report_to_merge_request


FORMAT_CMD = 'clang-format'
CPP_FILES_PATTERNS = ['*.c', '*.cpp', '*.cc', '*.C', '*.hpp', '*.h', '*.hh']


def check_clang_format():
    global FORMAT_CMD
    try:
        clang_format = local[FORMAT_CMD]
    except CommandNotFound as e:
        print('Cannot find command "{}":'.format(FORMAT_CMD), e)
        return False
    if clang_format:
        return True


def get_files_to_check(repository):
    is_ci = os.environ.get('GITLAB_CI', None)
    if is_ci:
        target_branch = os.environ.get('CI_MERGE_REQUEST_TARGET_BRANCH_NAME')
        if target_branch is None:
            return get_all_cpp_files(repository)
        return filter_files(get_changed_files(repository, target_branch))

    return get_all_cpp_files(repository)


def get_all_cpp_files(repository):
    global CPP_FILES_PATTERNS
    files = []
    for root, _, filenames in os.walk(repository):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    return filter_files(files)


def filter_files(files):
    global CPP_FILES_PATTERNS
    filtered_files = []
    for pattern in CPP_FILES_PATTERNS:
        filtered_files += list(fnmatch.filter(files, pattern))
    return filtered_files


def format_files(files):
    clang_format = local[FORMAT_CMD]
    for f in files:
        clang_format['-i', f]()


@click.command(help=__doc__)
@click.option('-r', 'repository', help="Path to repository", type=click.Path(exists=True), default=os.getcwd())
@click.option('-o', '--output', default='apply-formatting.patch', type=click.Path())
@click.option('--report', default='formatting.md', type=click.Path())
@click.option('--report-template', default=cpp_check_template, type=click.Path(exists=True))
@click.option('--exclude', type=click.Path(), multiple=True)
def cli(repository, output, report, report_template, exclude):
    if not check_clang_format():
        return -1
    files_to_check = get_files_to_check(repository)
    files_to_check = [f for f in files_to_check if f not in exclude]
    n_lines_changed = 0
    if files_to_check:
        format_files(files_to_check)
        n_lines_changed = create_patch(repository, output)

    if n_lines_changed > 0:
        changed_files = get_changed_files(repository, 'HEAD')
        create_report(repository, changed_files, output, report, template_file=report_template)
        add_report_to_merge_request([report])
        sys.exit(-1)

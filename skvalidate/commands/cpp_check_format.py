"""Check formatting of C++ code using clang-format"""

from __future__ import print_function
import os
import fnmatch


import click
from git import Repo
from plumbum import local
from plumbum.commands.processes import CommandNotFound

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
    repo = Repo(repository)
    git = repo.git
    if is_ci:
        target_branch = os.environ.get('CI_MERGE_REQUEST_TARGET_BRANCH_NAME')
        if target_branch is None:
            return get_all_cpp_files(repository)
        return get_changed_files(repository, target_branch)

    return get_all_cpp_files(repository)


def get_all_cpp_files(repository):
    global CPP_FILES_PATTERNS
    files = []
    for root, _, filenames in os.walk(repository):
        for filename in filenames:
            matches.append(os.path.join(root, filename))
    return filter_files(files)


def filter_files(files):
    global CPP_FILES_PATTERNS
    filtered_files = []
    for pattern in CPP_FILES_PATTERNS:
        filtered_files += list(fnmatch.filter(files, pattern))
    return filtered_files


def get_changed_files(repository, target_branch='FETCH_HEAD'):
    repo = Repo(repository)
    git = repo.git
    files = git.diff('--name-only', '--no-renames', '--diff-filter', 'MA', target_branch).split('\n')
    return filter_files(files)


def format_files(files):
    clang_format = local[FORMAT_CMD]
    for f in files:
        clang_format['-i', f]()


def create_patch(repository, output_file):
    repo = Repo(repository)
    git = repo.git
    diff = git.diff()
    with open(output_file, 'w') as f:
        f.write(diff)

    wc = local['wc']
    return int(wc['-l', output_file]().split()[0])


def create_report(changed_files, output_file, report_file):

    fix = 'curl ${CI_PROJECT_URL}/-/jobs/${CI_JOB_ID}/artifacts/raw/apply-formatting.patch | git am'


@click.command(help=__doc__)
@click.option('-r', 'repository', help="Path to repository", type=click.Path(), default=os.getcwd())
@click.option('-o', '--output', default='apply-formatting.patch', type=click.Path())
@click.option('--report', default='formatting.md', type=click.Path())
def cli(repository, output, report):
    if not check_clang_format():
        return -1
    files_to_check = get_files_to_check(repository)
    n_lines_changed = 0
    if files_to_check:
        format_files(files_to_check)
        n_lines_changed = create_patch(repository, output)

    if n_lines_changed > 0:
        changed_files = get_changed_files(repository, 'HEAD')
        create_report(changed_files, output, report)
    # curl ${CI_PROJECT_URL}/-/jobs/${CI_JOB_ID}/artifacts/raw/apply-formatting.patch | git am
    return n_lines_changed

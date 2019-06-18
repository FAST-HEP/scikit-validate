from __future__ import absolute_import
from git import Repo


def get_changed_files(repository, target_branch='FETCH_HEAD'):
    repo = Repo(repository)
    git = repo.git
    files = git.diff('--name-only', '--no-renames', '--diff-filter', 'MA', target_branch).split('\n')
    return files


def create_patch(repository, output_file):
    repo = Repo(repository)
    git = repo.git
    diff = git.diff()
    diff += '\n'

    if not diff.isspace():
        with open(output_file, 'w') as f:
            f.write(diff)
        return len(diff.split('\n'))
    return 0


def get_current_branch(repository):
    repo = Repo(repository)
    branch = None
    try:
        branch = str(repo.active_branch)
    except TypeError as e:
        if 'detached' in str(e):
            branch = 'detached HEAD'
    return branch

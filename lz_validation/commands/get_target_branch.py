"""
Script to extract the target branch for a given project and commit hash.

Meant to be run within a Gitlab CI job and needs the following ENV variables defined:

\b
 * CI_PROJECT_ID (automatic from CI job)
 * CI_COMMIT_SHA (automatic from CI job)
 * CI_API_TOKEN (to be set in the Gitlab project: settings -> pipelines -> add variable)

Related issue: https://gitlab.com/gitlab-org/gitlab-ce/issues/15280
"""
import os
import sys

import click

import gitlab


@click.command(help=__doc__)
def cli(args=None):
    ci_project_id = os.environ.get('CI_PROJECT_ID')
    ci_api_token = os.environ.get('CI_API_TOKEN')
    ci_commit_sha = os.environ.get('CI_COMMIT_SHA')

    connection = gitlab.Gitlab('https://lz-git.ua.edu/', ci_api_token, api_version=4)
    connection.auth()

    project = connection.projects.get(ci_project_id)
    mrs = project.mergerequests.list(state='opened')

    target_branch = None
    for mr in mrs:
        if mr.attributes['sha'] == ci_commit_sha:
            target_branch = mr.attributes['target_branch']

    if target_branch is None:
        print('Could not find matching MR')
        sys.exit(-1)
    click.echo(target_branch)

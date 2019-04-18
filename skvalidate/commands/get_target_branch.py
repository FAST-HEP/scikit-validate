"""
Script to extract the target branch for a given project and commit hash.

Meant to be run within a Gitlab CI job and needs the following ENV variables defined:

 * CI_PROJECT_ID (automatic from CI job)
 * CI_COMMIT_SHA (automatic from CI job)
 * CI_API_TOKEN (to be set in the Gitlab project: settings -> pipelines -> add variable)

Related issue: https://gitlab.com/gitlab-org/gitlab-ce/issues/15280

If no target branch is found, the command will try to fall back onto ``CI_COMMIT_REF_NAME``
if it is one of the tracked branches otherwise fallback onto the default branch (if defined)
or error if not
"""
import logging
import os
import sys

import click

import gitlab


# TODO: move gitlab bits to skvalidate.gitlab
@click.command(help=__doc__)
@click.option('--gitlab-server', default='gitlab.com')
@click.option('-t', '--tracked-branches', default=None)
@click.option('--default-branch', default=None)
def cli(gitlab_server, default_branch, tracked_branches):
    ci_project_id = os.environ.get('CI_PROJECT_ID')
    ci_api_token = os.environ.get('CI_API_TOKEN')
    ci_commit_sha = os.environ.get('CI_COMMIT_SHA')
    ci_commit_ref_name = os.environ.get('CI_COMMIT_REF_NAME')

    connection = gitlab.Gitlab(
        'https://{0}/'.format(gitlab_server),
        ci_api_token,
        api_version=4,
    )

    mrs = []
    target_branch = None
    gitlab_error = None
    try:
        connection.auth()
        project = connection.projects.get(ci_project_id)
        mrs = project.mergerequests.list(state='opened')
        for mr in mrs:
            if mr.attributes['sha'] == ci_commit_sha:
                target_branch = mr.attributes['target_branch']
    except gitlab.exceptions.GitlabHttpError:
        gitlab_error = 'Could not connect to {0}'.format(gitlab_server)

    target_branch = _pick_target_branch(target_branch, tracked_branches, default_branch, ci_commit_ref_name)

    if target_branch is None:
        if gitlab_error:
            logging.error(gitlab_error)
        logging.error('Could not find matching MR')
        sys.exit(-1)
    click.echo(target_branch)


def _pick_target_branch(target_branch, target_branches, default_branch, ci_commit_ref_name):
    if target_branch:
        return target_branch
    if target_branches and ci_commit_ref_name in target_branches:
        return ci_commit_ref_name
    if default_branch:
        return default_branch
    return None

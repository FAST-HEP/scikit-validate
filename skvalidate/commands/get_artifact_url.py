"""
Reads the ENV variable in a Gitlab CI job and constructs a URL for a given existing file or folder.

e.g.
    skvalidate get_artefact_url output/test_file

will return ${CI_PROJECT_URL}/-/jobs/${CI_JOB_ID}/artifacts/file/output/test_file

while
    skvalidate get_artefact_url output

will return ${CI_PROJECT_URL}/-/jobs/${CI_JOB_ID}/artifacts/browse/output
"""
import click
import os


@click.command(help=__doc__)
@click.argument('path', type=click.Path(exists=True))
def cli(path):
    CI_PROJECT_PATH = os.environ.get('CI_PROJECT_PATH', os.getcwd())
    CI_JOB_ID = os.environ.get('CI_JOB_ID')
    CI_PROJECT_URL = os.environ.get('CI_PROJECT_URL')
    url_template = '{CI_PROJECT_URL}/-/jobs/{CI_JOB_ID}/artifacts/{option}/{path}'

    path = path.replace(CI_PROJECT_PATH, '')

    option = 'browse'
    if os.path.isfile(path):
        option = 'file'
    return url_template.format(
        CI_PROJECT_URL=CI_PROJECT_URL,
        CI_JOB_ID=CI_JOB_ID,
        option=option,
        path=path,
    )

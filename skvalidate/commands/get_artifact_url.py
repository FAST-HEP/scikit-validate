"""
Reads the ENV variable in a Gitlab CI job and constructs a URL for a given existing file or folder.

e.g.

 .. code-block:: bash

    sv_get_artefact_url output/test_file

will return ``${CI_PROJECT_URL}/-/jobs/${CI_JOB_ID}/artifacts/file/output/test_file``

while

 .. code-block:: bash

    sv_get_artefact_url output

will return ``${CI_PROJECT_URL}/-/jobs/${CI_JOB_ID}/artifacts/browse/output``
"""
import click

from skvalidate.gitlab import get_artifact_url

# TODO: add RAW path option
@click.command(help=__doc__)
@click.argument('path', type=click.Path(exists=True))
def cli(path):
    return get_artifact_url(path)

import os
from collections import namedtuple
import pytest

from skvalidate.gitlab import path_and_job_id_to_artifact_url


@pytest.fixture()
def ci_project():
    Project = namedtuple('Project', ['path', 'job_id', 'url'])
    return Project(
        path='/builds/group/MyProject',
        job_id=42,
        url='https://gitlab.example.com/group/MyProject'
    )


@pytest.mark.parametrize('path,expected_url', [
    (
        '/builds/group/MyProject/file.json',
        'https://gitlab.example.com/group/MyProject/-/jobs/42/artifacts/file/file.json'
    ),
    (
        '/builds/group/MyProject/output/file.json',
        'https://gitlab.example.com/group/MyProject/-/jobs/42/artifacts/file/output/file.json'
    ),
    (
        '/builds/group/MyProject/output/../file.json',
        'https://gitlab.example.com/group/MyProject/-/jobs/42/artifacts/file/file.json'
    ),
])
def test_path_and_job_id_to_artifact_url(ci_project, path, expected_url):
    os.environ['CI_PROJECT_PATH'] = ci_project.path
    os.environ['CI_PROJECT_URL'] = ci_project.url
    url = path_and_job_id_to_artifact_url(path, ci_project.job_id, path_type='file')
    assert url == expected_url
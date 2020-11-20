import os
from collections import namedtuple
import gitlab
import pytest
import random
import json

import skvalidate.gitlab as sk_gl

@pytest.fixture()
def ci_project():
    Project = namedtuple('Project', ['path', 'job_id', 'url'])
    return Project(
        path=os.getcwd(),
        job_id=42,
        url='https://gitlab.example.com/group/MyProject'
    )


@pytest.fixture()
def ci_jobs():
    Job = namedtuple('Job', ['id', 'name'])
    jobs = []
    for i in range(5):
        jobs.append(Job(id=i + 100, name='build'))
        jobs.append(Job(id=i + 200, name='test'))
    random.shuffle(jobs)
    return jobs


@pytest.mark.parametrize('path,path_type,expected_url', [
    (
        'file.json',
        'file',
        'https://gitlab.example.com/group/MyProject/-/jobs/42/artifacts/file/file.json',
    ),
    (
        'file.json',
        'raw',
        'https://gitlab.example.com/group/MyProject/-/jobs/42/artifacts/raw/file.json',
    ),
    (
        os.getcwd() + '/output/file.json',
        'file',
        'https://gitlab.example.com/group/MyProject/-/jobs/42/artifacts/file/output/file.json'
    ),
    (
        os.getcwd() + '/output/../file.json',
        'file',
        'https://gitlab.example.com/group/MyProject/-/jobs/42/artifacts/file/file.json'
    ),
])
def test_path_and_job_id_to_artifact_url(ci_project, path, path_type, expected_url):
    os.environ['CI_PROJECT_PATH'] = ci_project.path
    os.environ['CI_PROJECT_URL'] = ci_project.url
    url = sk_gl.path_and_job_id_to_artifact_url(path, ci_project.job_id, path_type=path_type)
    assert url == expected_url


def test_select_last_iteration_only(ci_jobs):
    highest_build_id = max([j.id for j in ci_jobs if j.name == 'build'])
    highest_test_id = max([j.id for j in ci_jobs if j.name == 'test'])
    jobs = sk_gl._select_last_iteration_only(ci_jobs)
    assert len(jobs) == 2
    for job in jobs:
        if job.name == 'build':
            assert job.id == highest_build_id
        if job.name == 'test':
            assert job.id == highest_test_id


def test_download_artifact(gl, resp_artifact_json):
    sk_gl.GITLAB_CONNECTION = gl
    os.environ['CI_PROJECT_ID'] = '1'

    content = sk_gl.download_artifact(1, "test.json")
    assert json.loads(content) == {'name': 'value'}

def test_download_artifact_no_such_file(gl, resp_artifact_no_such_file):
    sk_gl.GITLAB_CONNECTION = gl
    os.environ['CI_PROJECT_ID'] = '1'

    with pytest.raises(gitlab.exceptions.GitlabGetError):
        sk_gl.download_artifact(1, "test.json")

def test_download_json_from_job(gl, resp_artifact_json):
    sk_gl.GITLAB_CONNECTION = gl
    os.environ['CI_PROJECT_ID'] = '1'

    content = sk_gl.download_json_from_job('test.json', 1)
    assert content == {'name': 'value'}

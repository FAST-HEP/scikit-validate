"""Module to implement interactions with GitLab.

Useful Gitlab variables (https://docs.gitlab.com/ee/ci/variables/):
 - CI_COMMIT_BEFORE_SHA
 - CI_COMMIT_REF_NAME
 - CI_COMMIT_SHA
 - CI_CONFIG_PATH
 - CI_JOB_ID
 - CI_JOB_NAME
 - CI_JOB_STAGE
 - CI_JOB_TOKEN
 - CI_JOB_URL
 - CI_MERGE_REQUEST_ID
 - CI_MERGE_REQUEST_IID
 - CI_PIPELINE_URL
 - CI_PIPELINE_ID
 - CI_PIPELINE_IID
 - CI_PROJECT_ID
 - CI_PROJECT_NAME
 - CI_PROJECT_URL
"""

import os

import gitlab
import json


GITLAB_CONNECTION = None


def _connect():
    global GITLAB_CONNECTION
    if GITLAB_CONNECTION is None:
        server_url, auth_token = _get_auth_data()
        GITLAB_CONNECTION = gitlab.Gitlab(server_url, auth_token, api_version=4)
        GITLAB_CONNECTION.auth()
    return GITLAB_CONNECTION


def _get_auth_data():
    project_url = os.environ.get('CI_PROJECT_URL')
    project_path = os.environ.get('CI_PROJECT_PATH')
    server_url = project_url.replace(project_path, '')
    auth_token = os.environ.get('READONLY_API_TOKEN')
    return server_url, auth_token


def get_jobs_for_stages(stages, **kwargs):
    """Collect job results for specified stages.

    @param stages: stages to get the jobs for

    @return
    {
        'status': 'passed|failed|warning',
        'link': '<link to CI job>',
        'link_raw': '<link to raw log file>,
        'software_versions': <list of all recorded software versions (from JSON)>,
        }
    """
    software_versions = kwargs.pop('software_versions', '')
    jobs = _get_current_pipeline_jobs()

    result = {}
    fields = ['name', 'status', 'duration', 'stage', 'web_url', 'id']
    for job in jobs:
        stage = job.attributes['stage']
        if stage not in stages:
            continue
        name = job.attributes['name']
        result[name] = {}
        for field in fields:
            result[name][field] = job.attributes[field]
        if software_versions:
            result[name]['software_versions'] = collect_software_versions(name, job.id, software_versions)
    return result


def _get_current_pipeline_jobs():
    connection = _connect()
    # get current pipeline
    CI_PROJECT_ID = os.environ.get('CI_PROJECT_ID')
    CI_PIPELINE_ID = os.environ.get('CI_PIPELINE_ID')
    project = connection.projects.get(CI_PROJECT_ID)
    pipeline = project.pipelines.get(CI_PIPELINE_ID)
    return pipeline.jobs.list()


def collect_software_versions(job_name, job_id, path):
    """Collect software_versions.json from specified stages.

    @param job_id: GitLab job ID for a pipeline job
    @param path: local path where software versions are stored
    """
    # download software_versions.json
    software_versions = download_artifact(job_id, path)
    # load
    data = json.loads(software_versions)
    result = []
    for software, version in data[job_name].items():
        result.append('{}={}'.format(software, version))

    return result


def download_artifact(job_id, path):
    connection = _connect()
    CI_PROJECT_ID = os.environ.get('CI_PROJECT_ID')
    project = connection.projects.get(CI_PROJECT_ID)
    job = project.jobs.get(job_id, lazy=True)
    # workaround for https://github.com/python-gitlab/python-gitlab/issues/683, fixed in python-gitlab 1.8.0
    # streamer = _Streamer()
    # job.artifact(path, streamed=True, action=streamer)
    # return streamer.content
    return job.artifact(path)


def get_artifact_url(local_path):
    CI_PROJECT_PATH = os.environ.get('CI_PROJECT_PATH', os.getcwd())
    CI_JOB_ID = os.environ.get('CI_JOB_ID')
    CI_PROJECT_URL = os.environ.get('CI_PROJECT_URL')
    url_template = '{CI_PROJECT_URL}/-/jobs/{CI_JOB_ID}/artifacts/{path_type}/{path}'

    local_path = local_path.replace(CI_PROJECT_PATH, '')

    path_type = 'browse'
    if os.path.isfile(local_path):
        path_type = 'file'
    return url_template.format(
        CI_PROJECT_URL=CI_PROJECT_URL,
        CI_JOB_ID=CI_JOB_ID,
        path_type=path_type,
        path=local_path,
    )


class _Streamer():

    def __init__(self):
        self.content = ''

    def __call__(self, chunk):
        self.content += str(chunk)

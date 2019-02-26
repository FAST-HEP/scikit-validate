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
        'name': 'job_name': {
            'status': 'success|failed',
            'web_url': '<link to CI job>',
            'web_url_raw': '<link to raw log file>,
            'software_versions': <list of all recorded software versions (from JSON)>,
            'id': job id,
        },
        ...
    }
    """
    download_json = kwargs.pop('download_json', {})
    job_filter = kwargs.pop('job_filter', [])
    jobs = _get_current_pipeline_jobs()

    result = {}
    fields = ['name', 'status', 'duration', 'stage', 'web_url', 'id']
    for job in jobs:
        stage = job.attributes['stage']
        if stage not in stages:
            continue
        name = job.attributes['name']
        if job_filter and name not in job_filter:
            continue
        result[name] = {}
        for field in fields:
            result[name][field] = job.attributes[field]
        # extras
        result[name]['web_url_raw'] = result[name]['web_url'] + '/raw'
        for j_name, j_path in download_json.items():
            result[name][j_name] = download_json_from_job(j_path, job.id)
    return result


def _get_current_pipeline_jobs():
    connection = _connect()
    # get current pipeline
    CI_PROJECT_ID = os.environ.get('CI_PROJECT_ID')
    CI_PIPELINE_ID = os.environ.get('CI_PIPELINE_ID')
    project = connection.projects.get(CI_PROJECT_ID)
    pipeline = project.pipelines.get(CI_PIPELINE_ID)
    return pipeline.jobs.list()


def download_json_from_job(json_file, job_id):
    """Collect JSON file from specified job and decode it.

    @param json_file: local path where software versions are stored
    @param job_id: GitLab job ID for a pipeline job
    """
    raw_json = download_artifact(job_id, json_file)
    # load
    try:
        data = json.loads(raw_json)
    except json.decoder.JSONDecodeError as e:
        print('Cannot parse {}'.format(raw_json))
        raise json.decoder.JSONDecodeError(str(e))
    return data


def download_artifact(job_id, path, output_file=None):
    connection = _connect()
    CI_PROJECT_ID = os.environ.get('CI_PROJECT_ID')
    project = connection.projects.get(CI_PROJECT_ID)
    job = project.jobs.get(job_id, lazy=True)
    # workaround for https://github.com/python-gitlab/python-gitlab/issues/683, fixed in python-gitlab 1.8.0
    streamer = None
    if output_file is None:
        streamer = _Streamer()
    else:
        streamer = _DiskStreamer(output_file)
    try:
        job.artifact(path, streamed=True, action=streamer)
        return streamer.content
    except gitlab.exceptions.GitlabGetError as e:
        print('Could not find artifact {} for job ID {}'.format(path, job_id))
        raise gitlab.exceptions.GitlabGetError(e)
    return None


def get_artifact_url(local_path):
    CI_PROJECT_PATH = os.environ.get('CI_PROJECT_PATH', os.getcwd())
    CI_JOB_ID = os.environ.get('CI_JOB_ID')
    local_path = local_path.replace(CI_PROJECT_PATH, '')

    path_type = 'browse'
    if os.path.isfile(local_path):
        path_type = 'file'
    return path_and_job_id_to_artifact_url(local_path, CI_JOB_ID, path_type)


def path_and_job_id_to_artifact_url(path, job_id, path_type='file'):
    CI_PROJECT_URL = os.environ.get('CI_PROJECT_URL')
    url_template = '{CI_PROJECT_URL}/-/jobs/{job_id}/artifacts/{path_type}/{path}'
    return url_template.format(
        CI_PROJECT_URL=CI_PROJECT_URL,
        job_id=job_id,
        path_type=path_type,
        path=path,
    )


def add_report_to_merge_request(report_file):
    with open(report_file) as f:
        content = f.read()

    project_id = os.environ.get('CI_PROJECT_ID')
    merge_request_id = os.environ.get('CI_MERGE_REQUEST_ID', None)
    if merge_request_id is None:
        print('This is not run as part of a merge request -- aborting ...')
        return
    project = GITLAB_CONNECTION.projects.get(project_id)
    mr = project.mergerequests.get(merge_request_id)
    # TODO: check if comment from user already exists, if yes --> update

    mr.notes.create(dict(
        body=content,
    ))

    mr.save()


def get_merge_request(project, mr_id):
    mr = project.mergerequests.get(mr_id)
    return mr

def add_label_to_merge_request(label, merge_request):
    merge_request.labels.append(label)
    merge_request.save()


def remove_label_from_merge_request(label, merge_request):
    merge_request.labels.remove(label)
    merge_request.save()


class _Streamer():

    def __init__(self):
        self.content = None

    def __call__(self, chunk):
        if self.content is None:
            self.content = chunk
        else:
            self.content += chunk


class _DiskStreamer():
    def __init__(self, output_file):
        self._f = open(output_file, 'wb')
        self.content = output_file

    def __call__(self, chunk):
        self._f.write(chunk)

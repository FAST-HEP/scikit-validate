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
import time

import gitlab
import json

from .. import logger
from skvalidate.io import create_directory


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

    :param stages: stages to get the jobs for
    :return: dictionary of jobs for the specified stages

    :Example:

    >>> get_jobs_for_stages(['build'])
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
    download_timeout = kwargs.pop('download_timeout', 60)
    job_filter = kwargs.pop('job_filter', [])
    jobs = _get_current_pipeline_jobs()

    result = {}
    fields = ['name', 'status', 'duration', 'stage', 'web_url', 'id']
    for job in jobs:
        stage = job.attributes['stage']
        if stage not in stages:
            logger.debug('Stage {0} not in [{1}]'.format(stage, ','.join(stages)))
            continue
        name = job.attributes['name']
        if job_filter and name not in job_filter:
            logger.debug('Job {0} not in [{1}]'.format(name, ','.join(job_filter)))
            continue
        result[name] = {}
        for field in fields:
            result[name][field] = job.attributes[field]
        # extras
        result[name]['web_url_raw'] = result[name]['web_url'] + '/raw'
        for j_name, j_path in download_json.items():
            result[name][j_name] = download_json_from_job(j_path, job.id, timeout=download_timeout)
    return result


def get_pipeline_job(job_name):
    jobs = _get_current_pipeline_jobs()
    selected_jobs = [job for job in jobs if job_name == job.attributes['name']]
    selected_jobs = sorted(selected_jobs, key=lambda j: j.id, reverse=True)
    if selected_jobs:
        return selected_jobs[0]  # first job should have highest ID --> latest
    return None


def _get_current_pipeline_jobs():
    connection = _connect()
    # get current pipeline
    CI_PROJECT_ID = os.environ.get('CI_PROJECT_ID')
    CI_PIPELINE_ID = os.environ.get('CI_PIPELINE_ID')
    project = connection.projects.get(CI_PROJECT_ID)
    pipeline = project.pipelines.get(CI_PIPELINE_ID)

    return _select_last_iteration_only(pipeline.jobs.list())


def _select_last_iteration_only(jobs):
    """
        Looks through a list of jobs and removes duplicates (only keeps last iteration of a particular job)
    """
    jobs_by_name = {}
    for job in jobs:
        if job.name in jobs_by_name:
            jobs_by_name[job.name].append(job)
        else:
            jobs_by_name[job.name] = [job]
    selected_jobs = []
    for name, named_jobs in jobs_by_name.items():
        named_jobs = sorted(named_jobs, key=lambda j: j.id, reverse=True)
        selected_jobs.append(named_jobs[0])
    return selected_jobs


def download_json_from_job(json_file, job_id, timeout=60):
    """Collect JSON file from specified job and decode it.

    :param json_file: local path where software versions are stored
    :param job_id: GitLab job ID for a pipeline job
    :param timeout: number of seconds to retry download for
    """
    raw_json = "{}"
    time_spent = 0
    wait_time = timeout // 10
    error = False
    while time_spent < timeout:
        time_spent += wait_time
        try:
            raw_json = download_artifact(job_id, json_file)
            error = False
        except gitlab.exceptions.GitlabHttpError as e:
            logger.error("Cannot download {} for job {}: {}".format(json_file, job_id, e))
            logger.error("Next attempt in {}s".format(wait_time))
            time.sleep(wait_time)
            error = True
    if time_spent > timeout and error:
        logger.error("Timeout exceeded for attempting to download {} for job {}".format(json_file, job_id))
        return {}
    # load
    try:
        data = json.loads(raw_json)
    except json.decoder.JSONDecodeError as e:
        logger.error('Cannot parse {}'.format(raw_json))
        raise json.decoder.JSONDecodeError(str(e))
    return data


def download_artifact(job_id, path, output_file=None):
    logger.debug('Downloading {0} from job #{1}'.format(path, job_id))
    if output_file and os.path.exists(output_file):
        logger.info('Output file {0} already exists, skipping download'.format(output_file))
        return None
    connection = _connect()
    CI_PROJECT_ID = os.environ.get('CI_PROJECT_ID')
    project = connection.projects.get(CI_PROJECT_ID)
    job = project.jobs.get(job_id, lazy=True)
    # workaround for https://github.com/python-gitlab/python-gitlab/issues/683, fixed in python-gitlab 1.8.0
    streamer = None
    if output_file is None:
        streamer = _Streamer()
    else:
        logger.debug('Saving {0} from job #{1} to {2}'.format(path, job_id, output_file))
        streamer = _DiskStreamer(output_file)
    try:
        job.artifact(path, streamed=True, action=streamer)
        return streamer.content
    except gitlab.exceptions.GitlabGetError as e:
        logger.error('Could not find artifact {} for job ID {}'.format(path, job_id))
        raise gitlab.exceptions.GitlabGetError(e)
    return None


def get_artifact_url(local_path):
    CI_JOB_ID = os.environ.get('CI_JOB_ID')
    path_type = 'browse'
    if os.path.isfile(local_path):
        path_type = 'file'
    return path_and_job_id_to_artifact_url(local_path, CI_JOB_ID, path_type)


def path_and_job_id_to_artifact_url(path, job_id, path_type='file'):
    CI_PROJECT_DIR = os.environ.get('CI_PROJECT_DIR', os.getcwd())
    CI_PROJECT_URL = os.environ.get('CI_PROJECT_URL')
    url_template = '{CI_PROJECT_URL}/-/jobs/{job_id}/artifacts/{path_type}/{path}'
    path = os.path.abspath(path)
    path = os.path.relpath(path, CI_PROJECT_DIR)
    path = os.path.normpath(path)

    return url_template.format(
        CI_PROJECT_URL=CI_PROJECT_URL,
        job_id=job_id,
        path_type=path_type,
        path=path,
    )


def add_or_update_comment_in_this_mr(content):
    is_ci = os.environ.get('GITLAB_CI', None)
    if is_ci is None:
        logger.warn('This is not run as part of the GitLab CI -- skipping ...')
        return
    mr = _get_merge_request()
    if mr is None:
        logger.warn('This is not run as part of a merge request -- skipping ...')
        return
    mr_notes = mr.notes.list()

    connection = _connect()
    current_user = connection.user
    existing_note = _note_from_user_exists(int(current_user.id), mr_notes)

    if existing_note is None:
        logger.debug('No existing comment found - creating new one ...')
        mr.notes.create(dict(body=content,))
    else:
        logger.debug('Found existing comment - modifying ...')
        # get editable note
        note = mr.notes.get(existing_note.id)
        note.body = content
        note.save()
    mr.save()


def _get_merge_request():
    is_ci = os.environ.get('GITLAB_CI', None)
    if is_ci is None:
        return None
    # CI_MERGE_REQUEST_ID is only available in runner version 11.6 and above
    # see https://docs.gitlab.com/ee/ci/variables/
    merge_request_id = os.environ.get('CI_MERGE_REQUEST_IID', None)

    project_id = os.environ.get('CI_PROJECT_ID')
    connection = _connect()
    project = connection.projects.get(project_id)

    if merge_request_id is not None:
        return project.mergerequests.get(merge_request_id)
    # otherwise, take the long way
    logger.warn('Running an outdated version of GitLab runner -- for full support use version >= 11.6')
    mrs = project.mergerequests.list(state='opened', order_by='updated_at')
    logger.debug('Found {0} open merge request(s)'.format(len(mrs)))
    ci_pipeline_id = int(os.environ.get('CI_PIPELINE_ID'))
    for mr in mrs:
        pipelines = mr.pipelines()
        for pipeline in pipelines:
            p_id = int(pipeline['id'])
            logger.debug('Found pipeline {0} for MR {1} (!{2})'.format(p_id, mr.id, mr.iid))
            if ci_pipeline_id == p_id:
                # It is not possible to edit or delete MergeRequest and GroupMergeRequest objects.
                # You need to create a ProjectMergeRequest object to apply changes:
                editable_mr = project.mergerequests.get(mr.iid, lazy=True)
                return editable_mr
    logger.warn('No matching merge request found for pipeline {0}'.format(ci_pipeline_id))
    return None


def _note_from_user_exists(user_id, notes):
    note_found = None
    for note in notes:
        note_user_id = int(note.author['id'])
        if note_user_id == user_id:
            note_found = note
            break
    return note_found


def get_merge_request(project, mr_id):
    mr = project.mergerequests.get(mr_id)
    return mr


def add_label_to_merge_request(label, merge_request):
    merge_request.labels.append(label)
    merge_request.save()


def remove_label_from_merge_request(label, merge_request):
    merge_request.labels.remove(label)
    merge_request.save()


def get_pipeline_url():
    is_ci = os.environ.get('GITLAB_CI', None)
    if is_ci is None:
        return "Pipeline URL not found"
    # try via new variable (Gitlab > 11.0)
    pipeline_url = os.environ.get('CI_PIPELINE_URL', None)
    if pipeline_url is not None:
        return pipeline_url
    # try via project URL and pipeline ID
    project_url = os.environ.get('CI_PROJECT_URL')
    pipeline_id = os.environ.get('CI_PIPELINE_ID')
    pipeline_url = project_url + '/pipelines/' + str(pipeline_id)
    return pipeline_url


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
        directory = os.path.split(output_file)[:-1]
        directory = os.path.join(*directory)
        create_directory(directory)

        self._f = open(output_file, 'wb')
        self.content = output_file

    def __call__(self, chunk):
        self._f.write(chunk)

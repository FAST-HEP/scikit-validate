import os

# import gitlab


def get_jobs_for_stage(stage):
    pass


def get_artifact_url(local_path):
    CI_PROJECT_PATH = os.environ.get('CI_PROJECT_PATH', os.getcwd())
    CI_JOB_ID = os.environ.get('CI_JOB_ID')
    CI_PROJECT_URL = os.environ.get('CI_PROJECT_URL')
    url_template = '{CI_PROJECT_URL}/-/jobs/{CI_JOB_ID}/artifacts/{option}/{path}'

    local_path = local_path.replace(CI_PROJECT_PATH, '')

    option = 'browse'
    if os.path.isfile(local_path):
        option = 'file'
    return url_template.format(
        CI_PROJECT_URL=CI_PROJECT_URL,
        CI_JOB_ID=CI_JOB_ID,
        option=option,
        path=local_path,
    )

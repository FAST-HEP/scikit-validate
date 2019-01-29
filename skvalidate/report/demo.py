"""Dummy package for testing & examples."""
from ..io import read_data_from_json

DEMO_SERVER = 'gitlab.example.com'
DEMO_GROUP = 'secret'
DEMO_PROJECT = 'enigma'
DEMO_PIPELINE_ID = 42
DEMO_JOB_ID = 123


def get_pipeline_url():
    tmp = 'https://{server}/{group}/{project}/pipelines/{p_id}'
    return tmp.format(
        server=DEMO_SERVER,
        group=DEMO_GROUP,
        project=DEMO_PROJECT,
        p_id=DEMO_PIPELINE_ID,
    )


def get_output_url():
    tmp = 'https://{server}/{group}/{project}/-/jobs/{j_id}/artifacts/browse'
    return tmp.format(
        server=DEMO_SERVER,
        group=DEMO_GROUP,
        project=DEMO_PROJECT,
        j_id=DEMO_JOB_ID,
    )


def get_jobs_for_stages(stages, **kwargs):
    jobs = {}
    software_versions = {}
    if 'software_versions' in kwargs:
        software_versions = _get_software_versions(kwargs.pop('software_versions'))

    for stage in stages:
        jobs.update(get_jobs_for_stage(stage, software_versions=software_versions, **kwargs))

    return jobs


def get_jobs_for_stage(stage, **kwargs):
    tmp = 'https://{server}/{group}/{project}/-/jobs/{j_id}'
    suffix_raw = '/raw'
    link = tmp.format(
        server=DEMO_SERVER,
        group=DEMO_GROUP,
        project=DEMO_PROJECT,
        j_id=1,
    )
    link_raw = link + suffix_raw

    software_versions = {}
    if 'software_versions' in kwargs:
        software_versions = kwargs.pop('software_versions')

    symbol_ok = 'passed'
    symbol_fail = 'failed'
    if 'symbol_ok' in kwargs:
        symbol_ok = kwargs.pop('symbol_ok')
    if 'symbol_fail' in kwargs:
        symbol_fail = kwargs.pop('symbol_fail')

    result = {}
    if stage == 'build':
        result = _get_builds(link, link_raw, software_versions)
    elif stage == 'test':
        result = _get_tests(link, link_raw, software_versions)
    elif stage == 'validation':
        result = _get_validations(link, link_raw, software_versions)

    return _format_status(result, symbol_ok, symbol_fail)


def _get_builds(link, link_raw, software_versions):
    versions1 = software_versions['build1'] if 'build1' in software_versions else ['---']
    versions2 = software_versions['build2'] if 'build2' in software_versions else ['---']
    return {
        'build1': {'status': 'passed', 'link': link, 'link_raw': link_raw, 'software_versions': versions1},
        'build2': {'status': 'failed', 'link': link, 'link_raw': link_raw, 'software_versions': versions2},
    }


def _get_tests(link, link_raw, software_versions):
    versions1 = software_versions['test1'] if 'test1' in software_versions else ['---']
    versions2 = software_versions['test2'] if 'test2' in software_versions else ['---']
    return {
        'test1': {'status': 'passed', 'link': link, 'link_raw': link_raw, 'software_versions': versions1},
        'test2': {'status': 'failed', 'link': link, 'link_raw': link_raw, 'software_versions': versions2},
    }


def _get_validations(link, link_raw, software_versions):
    versions1 = software_versions['validation1'] if 'validation1' in software_versions else ['---']
    versions2 = software_versions['validation2'] if 'validation2' in software_versions else ['---']
    return {
        'validation1': {'status': 'failed', 'link': link, 'link_raw': link_raw, 'software_versions': versions1},
        'validation2': {'status': 'passed', 'link': link, 'link_raw': link_raw, 'software_versions': versions2},
    }


def _format_status(items, symbol_ok, symbol_fail):
    result = {}
    for name, content in items.items():
        result[name] = content
        if content['status'] == 'passed':
            result[name]['status'] = symbol_ok
        if content['status'] == 'failed':
            result[name]['status'] = symbol_fail
    return result


def _get_software_versions(software_versions):
    result = {}
    data = read_data_from_json(software_versions)
    for job, versions in data.items():
        result[job] = []
        for software, version in versions.items():
            result[job].append('{}={}'.format(software, version))
    return result

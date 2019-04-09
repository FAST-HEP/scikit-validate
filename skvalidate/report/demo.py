"""Dummy package for testing & examples."""
from ..io import read_data_from_json
from . import format_status, format_software_versions, validation

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
    web_url = tmp.format(
        server=DEMO_SERVER,
        group=DEMO_GROUP,
        project=DEMO_PROJECT,
        j_id=1,
    )
    web_url_raw = web_url + suffix_raw

    software_versions = {}
    if 'software_versions' in kwargs:
        software_versions = kwargs.pop('software_versions')

    symbol_success = 'success'
    symbol_failed = 'failed'
    if 'symbol_success' in kwargs:
        symbol_success = kwargs.pop('symbol_success')
    if 'symbol_failed' in kwargs:
        symbol_failed = kwargs.pop('symbol_failed')

    result = {}
    if stage == 'build':
        result = _get_builds(web_url, web_url_raw, software_versions)
    elif stage == 'test':
        result = _get_tests(web_url, web_url_raw, software_versions)
    elif stage == 'validation':
        result = _get_validations(web_url, web_url_raw, software_versions)

    return format_status(result, symbol_success, symbol_failed)


def _get_builds(web_url, web_url_raw, software_versions):
    versions1 = software_versions['build1'] if 'build1' in software_versions else ['---']
    versions2 = software_versions['build2'] if 'build2' in software_versions else ['---']
    return {
        'build1': {'status': 'passed', 'web_url': web_url, 'web_url_raw': web_url_raw, 'software_versions': versions1},
        'build2': {'status': 'failed', 'web_url': web_url, 'web_url_raw': web_url_raw, 'software_versions': versions2},
    }


def _get_tests(web_url, web_url_raw, software_versions):
    versions1 = software_versions['test1'] if 'test1' in software_versions else ['---']
    versions2 = software_versions['test2'] if 'test2' in software_versions else ['---']
    return {
        'test1': {'status': 'passed', 'web_url': web_url, 'web_url_raw': web_url_raw, 'software_versions': versions1},
        'test2': {'status': 'failed', 'web_url': web_url, 'web_url_raw': web_url_raw, 'software_versions': versions2},
    }


def _get_validations(web_url, web_url_raw, software_versions):
    versions1 = software_versions['validation1'] if 'validation1' in software_versions else ['---']
    versions2 = software_versions['validation2'] if 'validation2' in software_versions else ['---']
    return {
        'validation1': {
            'status': 'failed', 'web_url': web_url, 'web_url_raw': web_url_raw, 'software_versions': versions1
        },
        'validation2': {
            'status': 'passed', 'web_url': web_url, 'web_url_raw': web_url_raw, 'software_versions': versions2
        },
    }


def get_full_validations(**kwargs):
    validation_detail = kwargs.pop('validation_detail')

    data = {}
    for name, json_file in validation_detail.items():
        data[name] = read_data_from_json(json_file)['root_diff']
        data[name]['images'] = []
        for _, info in data[name]['distributions'].items():
            if 'image' in info:
                data[name]['images'].append(info['image'])
        validation_output_file = 'validation_report_{0}'.format(name)
        details = validation.create_detailed_report(
            data[name], output_dir='.', output_file=validation_output_file, formats=['md', 'pdf'])
        data[name]['web_url_to_details'] = details
    summary = validation.create_summary(data)

    symbol_success = kwargs.pop('symbol_success', 'success')
    symbol_failed = kwargs.pop('symbol_failed', 'failed')

    result = format_status(summary, symbol_success, symbol_failed)
    return format_software_versions(result)


def _get_software_versions(software_versions):
    result = {}
    data = read_data_from_json(software_versions)
    for job, versions in data.items():
        result[job] = []
        for software, version in versions.items():
            result[job].append('{}={}'.format(software, version))
    return result

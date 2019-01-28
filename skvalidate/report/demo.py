""" Dummy package for testing & examples """
import json

from ..compare import compare_metrics

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

    symbol_ok = 'passed'
    symbol_fail = 'failed'
    if 'symbol_ok' in kwargs:
        symbol_ok = kwargs.pop('symbol_ok')
    if 'symbol_fail' in kwargs:
        symbol_fail = kwargs.pop('symbol_fail')

    result = {}
    if stage == 'build':
        result = _get_builds(link, link_raw)
    elif stage == 'test':
        result = _get_tests(link, link_raw)

    return _format_status(result, symbol_ok, symbol_fail)


def _get_builds(link, link_raw):
    return {
        'build1': {'status': 'passed', 'link': link, 'link_raw': link_raw},
        'build2': {'status': 'failed', 'link': link, 'link_raw': link_raw},
    }


def _get_tests(link, link_raw):
    return {
        'test1': {'status': 'passed', 'link': link, 'link_raw': link_raw},
        'test2': {'status': 'failed', 'link': link, 'link_raw': link_raw},
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


def get_metrics(metrics_json, metrics_ref_json, **kwargs):
    with open(metrics_json) as f:
        metrics = json.load(f)
    with open(metrics_ref_json) as f:
        metrics_ref = json.load(f)

    keys = kwargs.pop('keys', None)
    comparison = compare_metrics(metrics, metrics_ref, keys=keys)
    # format metrics
    symbol_up = kwargs.pop('symbol_up', '')
    symbol_down = kwargs.pop('symbol_down', '')
    symbol_same = kwargs.pop('symbol_same', '')

    tmp = '{:2f}% {}'

    for cmd, metrics in comparison.items():
        for name, metric in metrics.items():
            if isinstance(metric['diff'], str):
                metric['symbol'] = ''
                continue
            if metric['diff'] > 0:
                metric['symbol'] = symbol_up
            elif metric['diff'] < 0:
                metric['symbol'] = symbol_down
            else:
                metric['symbol'] = symbol_same

    return comparison


def software_versions(**kwargs):
    return {}

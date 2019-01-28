from __future__ import division
import numpy as np
from skvalidate.io import walk


def difference(a1, a2):
    try:
        # convert to float64 to avoid hitting int limits
        new_type = a1.dtype
        if np.issubdtype(new_type, np.integer):
            new_type = np.float64
        return np.subtract(a1.flatten().astype(new_type), a2.flatten().astype(new_type))
    except Exception:
        # TODO: need to compare string as well?
        return []


def is_ok(diff, normalisation, tolerance=0.02):
    d = np.absolute(diff)

    if abs(normalisation) == np.Infinity or np.Infinity in d:
        return False
    if normalisation == 0:
        return True

    return max(d / normalisation) <= tolerance


def compare_two_root_files(file1, file2, tolerance=0.02):
    are_ok = []
    are_not_ok = []

    content1 = dict((key, value) for (key, value) in walk(file1))
    content2 = dict((key, value) for (key, value) in walk(file2))
    keys1 = set(content1.keys())
    keys2 = set(content2.keys())

    all_keys = sorted(keys1 | keys2)

    for name in all_keys:
        value1 = content1[name] if name in content1 else np.array([np.Infinity])
        value2 = content2[name] if name in content2 else np.array([np.Infinity])

        diff = difference(value2, value1)
        if not len(diff):
            are_not_ok.append((name, (value1, value2, diff)))
            continue
        norm = np.sqrt(np.sum(value2**2))
        if not is_ok(diff, normalisation=norm, tolerance=tolerance):
            are_not_ok.append((name, (value1, value2, diff)))
        else:
            are_ok.append((name, (value1, value2, diff)))
    return are_ok, are_not_ok


def compare_metrics(metrics, metrics_ref, keys=None):
    """Compare two sets of metrics (nominal and reference).

    @param metrics: dictionary of metrics
    @param metrics_ref: dictionary of reference metrics
    @param keys: list of metrics to consider

    metrics format:
    {
        'metric description' :{
            'metric name':{
                'value': <float or int>,
                'unit': 'unit of measurement'
            },
            ...
        },
        ...
    }
    """
    # metrics = json.load(metrics_json)
    # metrics_ref = json.load(metrics_json_ref)
    if keys is None:
        keys = list(metrics_ref.values())[0].keys()

    all_metrics = list(metrics.keys()) + list(metrics_ref.keys())
    results = {}
    missing = '---'

    for metric in all_metrics:
        results[metric] = {}
        content = metrics[metric] if metric in metrics else missing
        content_ref = metrics_ref[metric] if metric in metrics_ref else missing
        for k in keys:
            results[metric][k] = {}
            value = content[k]['value'] if k in content else missing
            ref = content_ref[k]['value'] if k in content_ref else missing
            unit = content[k]['unit'] if k in content and 'unit' in content[k] else ''
            results[metric][k]['unit'] = unit
            results[metric][k]['value'] = value
            results[metric][k]['ref'] = ref
            try:
                results[metric][k]['diff'] = value - ref
                results[metric][k]['diff_pc'] = (value - ref) / ref * 100
            except (TypeError, ValueError, ZeroDivisionError) as _:
                results[metric][k]['diff'] = missing
                results[metric][k]['diff_pc'] = missing
    return results

from __future__ import division


def compare_metrics(metrics, metrics_ref, keys=None):
    """Compare two sets of metrics (nominal and reference).

    :param metrics: dictionary of metrics
    :param metrics_ref: dictionary of reference metrics
    :param keys: list of metrics to consider

    :Example:

    >>> compare_metrics(metrics, metrics_ref)
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
    metrics = convert_old_to_new(metrics)
    metrics_ref = convert_old_to_new(metrics_ref)
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
            except (TypeError, ValueError, ZeroDivisionError):
                results[metric][k]['diff'] = missing
                results[metric][k]['diff_pc'] = missing
    return results


def convert_old_to_new(metrics_collection):
    """Convert old metric format to new oneself.

    :Example:

    >>> old_metric
    {
        "file1": {
            "size_in_bytes": 84890132,
            "size_in_mb": 81.0,
        }
    }
    >>> convert_old_to_new(old_metric)
    {
        "file1": {
            "size_in_bytes": {'value': 84890132, 'unit': ''},
            "size_in_mb": {'value': 81.0, 'unit': ''},
        }
    }
    """
    new_style_metrics = {}
    for name, metrics in metrics_collection.items():
        new_style_metrics[name] = {}
        for metric_name, metric in metrics.items():
            new_style_metrics[name][metric_name] = {}
            if not isinstance(metric, dict):
                new_style_metrics[name][metric_name]['value'] = metric
            else:
                new_style_metrics[name][metric_name] = metric
            if 'unit' not in new_style_metrics[name][metric_name]:
                new_style_metrics[name][metric_name]['unit'] = ''

    return new_style_metrics


def absolute_to_relative_timestamps(profile):
    """Change timestamps from absolute to relative times.

    :param profile: a memory profile dictionary from memory_profiler
    """
    timestamps = profile['timestamp']
    baseline = timestamps[0]
    profile['timestamp'][:] = [x - baseline for x in timestamps]
    return profile

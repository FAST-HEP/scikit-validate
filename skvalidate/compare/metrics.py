from __future__ import division
import json

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
                print(results[metric][k]['diff_pc'])
            except (TypeError, ValueError, ZeroDivisionError) as _:
                results[metric][k]['diff'] = missing
                results[metric][k]['diff_pc'] = missing
    return results

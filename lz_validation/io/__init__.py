"""Module for any IO operations."""
import json
import os


def save_metrics_to_file(metrics, metrics_file):
    if os.path.exists(metrics_file):
        with open(metrics_file) as f:
            metrics.update(json.load(f))
    with open(metrics_file, 'w') as f:
        json.dump(metrics, f)


def root_walk(obj):
    for k in sorted(obj.allkeys()):
        if not obj[k].fBranches:
            yield k.decode("utf-8"), obj[k]
        else:
            for name, branch in root_walk(obj[k]):
                yield '{0}.{1}'.format(k.decode("utf-8"), name), branch

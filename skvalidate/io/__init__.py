"""Module for any IO operations."""
import json
import os
import numpy as np
import uproot


def save_metrics_to_file(metrics, metrics_file):
    if os.path.exists(metrics_file):
        with open(metrics_file) as f:
            metrics.update(json.load(f))
    with open(metrics_file, 'w') as f:
        json.dump(metrics, f)


def walk(path_to_root_file):
    f = uproot.open(path_to_root_file)
    return _walk(f)


def _walk(obj):
    for k in sorted(obj.allkeys()):
        try:
            yield k.decode("utf-8"), obj[k].array()
        except Exception:
            for n, o in _walk(obj[k]):
                yield '{0}.{1}'.format(k.decode("utf-8"), n), o


def save_array_to_file(array, name, output_dir):
    output_file = os.path.join(output_dir, name + '.npy')
    np.save(output_file, array)

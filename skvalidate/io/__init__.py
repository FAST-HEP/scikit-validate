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
    for name, obj in _walk(f):
        for subname, subobj in unpack(name, obj):
            yield subname, subobj


def _walk(obj, name=None):
    if not obj.keys():
        yield name, obj
    else:
        for k in sorted(obj.keys()):
            # if there is a '.' the first part of k it will be a duplicate
            new_k = k.decode("utf-8").split('.')[-1]
            new_name = '.'.join([name, new_k]) if name else new_k
            for n, o in _walk(obj[k], new_name):
                yield n, o


def unpack(name, obj):
    try:
        array = obj.array()
    except Exception:
        yield name, []
        return

    if hasattr(array, 'flatten'):
        flat_array = obj.array().flatten()
    else:
        flat_array = array

    if flat_array.__class__.__name__ == 'ObjectArrayMethods':
        o = flat_array[0]
        attributes = [x for x in dir(o) if x.startswith('_f')]
        for a in attributes:
            yield name + '.' + a, np.asarray([getattr(x, a) for x in flat_array])
    else:
        yield name, flat_array


def save_array_to_file(array, name, output_dir):
    output_file = os.path.join(output_dir, name + '.npy')
    np.save(output_file, array)

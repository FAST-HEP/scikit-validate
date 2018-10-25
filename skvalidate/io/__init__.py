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


def _walk(obj):
    seen = set()

    def _step(obj):
        for k in sorted(obj.allkeys()):
            value = obj[k]
            if hasattr(value, '_streamer') and 'TStreamerInfo' not in value._streamer.__class__.__name__:
                obj_id = id(value._streamer)
                if obj_id in seen and value._streamer is not None:
                    continue
                seen.add(obj_id)
                yield k.decode("utf-8"), value
            else:
                for n, o in _step(value):
                    yield '{0}.{1}'.format(k.decode("utf-8"), n), o
    return _step(obj)


def unpack(name, obj):
    flat_array = obj.array(flatten=True)

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

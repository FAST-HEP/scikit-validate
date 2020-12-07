"""Module for any IO operations."""
import glob
import json
import os
import requests

from mprof import read_mprofile_file
import numpy as np
import uproot
import awkward as ak
from fuzzywuzzy import process

from .. import logger
import skvalidate.operations._awkward as skak


def save_metrics_to_file(metrics, metrics_file):
    update_data_in_json(metrics, metrics_file)


def update_data_in_json(data, json_file):
    if os.path.exists(json_file):
        with open(json_file) as f:
            data.update(json.load(f))
    write_data_to_json(data, json_file)


def write_data_to_json(data, json_file):
    with open(json_file, 'w') as f:
        json.dump(data, f, indent=4, default=_unpack_numpy_arrays)


def _unpack_numpy_arrays(obj):
    """From https://stackoverflow.com/questions/26646362/numpy-array-is-not-json-serializable"""
    if type(obj).__module__ == np.__name__:
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return obj.item()
    raise TypeError('Unknown type:', type(obj))


def read_data_from_json(json_file):
    with open(json_file, 'r') as f:
        return json.load(f)


def walk(path_to_root_file, unpack_fields=True):
    f = uproot.open(path_to_root_file)
    for name, obj in _walk(f):
        if not unpack_fields:
            yield name, obj
            continue
        for subname, subobj in unpack(name, obj):
            yield subname, subobj


def _walk(obj, name=None):
    if not hasattr(obj, 'keys') or len(obj.keys()) == 0:
        yield name, obj
    else:
        for k in sorted(obj.keys(recursive=False)):
            # if there is a '.' the first part of k it will be a duplicate
            tokens = k.split('.')
            new_name = name if name else k
            for t in tokens:
                if new_name.endswith(t):
                    continue
                new_name = '.'.join([new_name, t])
            for n, o in _walk(obj[k], new_name):
                yield n, o


def unpack(name, obj):
    try:
        array = obj.array()
    except Exception:
        yield name, []
        return

    try:
        flat_array = ak.flatten(obj.array())
    except ValueError as e:
        logger.debug('Cannot flatten {}: {}'.format(name, e))
        flat_array = obj.array()
    else:
        flat_array = array

    unpacked = skak.unpack_array(flat_array)
    if not isinstance(unpacked, dict):
        yield name, flat_array
        return

    for field, value in unpacked.items():
        yield name + '.' + field, value


def save_array_to_file(array, name, output_dir):
    output_file = os.path.join(output_dir, name + '.npy')
    np.save(output_file, array)


def resolve_wildcard_path(wildcard_path):
    files = glob.glob(wildcard_path)
    for f in files:
        yield os.path.abspath(f)


def download_file(url, output):
    if url.startswith('gitlab://'):
        download_from_gitlab(url, output)
    else:
        _download_file(url, output)


def download_from_gitlab(url, output):
    from skvalidate import gitlab
    url = url.replace('gitlab://', '')
    tokens = url.split('/')
    job_name = tokens[0]
    file_path = os.path.join(*tokens[1:])
    logger.debug(f'Attempting to download file "{file_path}" from pipeline job "{job_name}"')

    job = gitlab.get_pipeline_job(job_name)
    gitlab.download_artifact(job.id, path=file_path, output_file=output)


def _download_file(url, output):
    r = requests.get(url)
    r.raise_for_status()

    directory = os.path.split(output)[:-1]
    directory = os.path.join(directory)
    create_directory(directory)

    with open(output, 'wb') as f:
        f.write(r.content)


def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def split_memory_profile_output(profile_file):
    profiles = {}
    command = None
    command_token = 'CMDLINE '
    logger.debug('Opening memory profile file: {0}'.format(profile_file))
    with open(profile_file) as f:
        for line in f.readlines():
            if line.startswith(command_token):
                command = line.replace(command_token, '')
                profiles[command] = []
                continue
            if command:
                profiles[command].append(line)
    file_nr = 0
    results = {}
    for command, lines in profiles.items():
        # TODO: move to /tmp
        output_file = profile_file + '.' + str(file_nr)
        file_nr += 1
        logger.debug('Splitting {0} into {1}'.format(profile_file, output_file))
        with open(output_file, 'w') as f:
            f.write(command_token + command)
            f.write(''.join(lines))
        profile = read_mprofile_file(output_file)
        results[command.strip('\n')] = dict(
            mem_usage=profile['mem_usage'],
            timestamp=profile['timestamp']
        )
    return results


def recursive_keys(path_to_root_file, unpack_fields=True):
    f = uproot.open(path_to_root_file)
    for name, obj in _walk(f):
        if not unpack_fields:
            yield name
            del obj
            continue
        for subname, _ in unpack(name, obj):
            yield subname
        del obj


def load_array(path_to_root_file, array_name):
    f = uproot.open(path_to_root_file)
    tokens = array_name.split('.')
    obj = f[tokens[0]]
    try:  # fuzzy match
        tmp_key = '/'.join(tokens[1:])
        key, _ = process.extractOne(tmp_key, obj.keys())
        obj = obj[key]
    except Exception:  # dig deeper
        for t in tokens[1:]:
            obj = obj[t]

    if hasattr(obj, 'array'):
        array = obj.array()
        try:  # to unpack array
            array = getattr(array, tokens[-1])
        except Exception:
            pass
        return array
    return obj

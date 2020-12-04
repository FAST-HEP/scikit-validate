from __future__ import division
import numexpr as ne
import numpy as np
from scipy import stats

import awkward as ak

from skvalidate.io import recursive_keys, load_array
from .metrics import compare_metrics, absolute_to_relative_timestamps
from .. import logger
import skvalidate.operations._awkward as skak # noqa F405

SUCCESS = 'success'
FAILED = 'failed'
UNKNOWN = 'unknown'
ERROR = 'error'


def difference(a1, a2):
    a1_tmp, a2_tmp = _ensure_same_lentgth(a1, a2)
    if hasattr(a1, 'dtype'):
        if np.issubdtype(a1.dtype, np.str_):
            return []

    return np.subtract(a1_tmp, a2_tmp)


def _ensure_same_lentgth(a1, a2):
    a1_size, a2_size = np.size(a1), np.size(a2)
    if a1_size == a2_size:
        return a1, a2
    if a1_size > a2_size:
        return a1, np.resize(a2, a1_size)
    if a2_size > a1_size:
        return np.resize(a1, a2_size), a2


def is_ok(evaluationFunc, cut, *args, **kwargs):
    value = evaluationFunc(*args, **kwargs)  # noqa: F841
    return np.all(ne.evaluate(cut))


def compare_two_root_files(file1, file2, tolerance=0.02):
    """Compare two ROOT(.cern.ch) files and return dictionary of comparison."""
    comparison = {}
    # content1 = dict((key, value) for (key, value) in walk(file1))
    # content2 = dict((key, value) for (key, value) in walk(file2))
    keys1 = set(recursive_keys(file1))
    keys2 = set(recursive_keys(file2))
    all_keys = sorted(keys1 | keys2)
    print(f'Testing {len(all_keys)} distributions')
    # for name in tqdm(all_keys): # tqdm does not work well inside CI
    for name in all_keys:
        comparison[name] = {}
        status = FAILED
        evaluationValue, ks_statistic, pvalue = 0, 0, 0
        diff = np.array([])
        reason = ''

        evaluationFunc = maxRelativeDifference
        cut = 'value <= {}'.format(tolerance)

        value1 = load_value(name, file1, keys1)
        value2 = load_value(name, file2, keys2)

        try:
            v1_size = np.size(value1)
            v2_size = np.size(value2)
        except Exception:
            print(f'Cannot handle {name} due to issues with value.size')
            continue
        if len(value1) == 0 and len(value2) == 0:
            status = SUCCESS
            pvalue = 1
        elif (v1_size == 0 and v2_size > 0) or (v1_size > 0 and v2_size == 0):
            status = FAILED
            reason = 'original file is empty' if v1_size > 0 else 'reference file is empty'
            diff = value1 if v1_size > 0 else value2
        elif value1 is None or value2 is None:
            status = UNKNOWN
            reason = 'Cannot convert data to numpy array'
        else:
            ks_statistic, pvalue = stats.ks_2samp(ak.to_numpy(value2), ak.to_numpy(value1))

            try:
                diff = difference(value2, value1)
                evaluationValue = evaluationFunc(value1, value2)
                status = evaluateStatus(value1, value2, evaluationFunc, cut)
                if status == FAILED:
                    reason = f'evaluationFunc({evaluationValue} > {cut}) failed'
            except Exception as e:
                reason = str(e)
                status = UNKNOWN
        yield name, dict(
            status=status,
            original=value1,
            reference=value2,
            diff=diff,
            evaluationValue=evaluationValue,
            ks_statistic=ks_statistic,
            pvalue=pvalue,
            reason=reason,
        )


def load_value(name, file_name, keys):
    value = load_array(file_name, name) if name in keys else ak.Array([])
    if hasattr(value, 'array'):
        value = value.array()
    try:
        value = ak.flatten(value)
    except ValueError:
        pass
    return value


def evaluateStatus(value1, value2, evaluationFunc, cut):
    status = FAILED
    if is_ok(evaluationFunc, cut=cut, value1=value1, value2=value2):
        status = SUCCESS
    return status


def norm(data):
    return np.sqrt(np.sum(abs(data * data)))


def maxRelativeDifference(value1, value2, normalisation=None):
    diff = difference(value2, value1)
    d = np.absolute(diff)
    if normalisation is None:
        normalisation = value2 if np.size(value2) > 0 else value1
        normalisation = norm(normalisation)

    if abs(normalisation) == np.Infinity or np.Infinity in d:
        return np.Infinity
    if normalisation == 0:
        return 0

    return np.amax(d / normalisation)


def reset_infinities(values):
    try:
        values[np.absolute(values) == np.Infinity] = 0
    except Exception as e:
        logger.error('Cannot process', ak.type(values))
        raise e
    return values


__all__ = [
    'absolute_to_relative_timestamps',
    'compare_metrics',
    'compare_two_root_files',
]

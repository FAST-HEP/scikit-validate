from __future__ import division
import numexpr as ne
import numpy as np
from scipy import stats

from skvalidate.io import walk
from .metrics import compare_metrics, absolute_to_relative_timestamps

SUCCESS = 'success'
FAILED = 'failed'
UNKNOWN = 'unknown'
ERROR = 'error'


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


def is_ok(evaluationFunc, cut, *args, **kwargs):
    value = evaluationFunc(*args, **kwargs)  # noqa: F841
    return np.all(ne.evaluate(cut))


def compare_two_root_files(file1, file2, tolerance=0.02):
    """Compare two ROOT(.cern.ch) files and return dictionary of comparison."""
    comparison = {}

    content1 = dict((key, value) for (key, value) in walk(file1))
    content2 = dict((key, value) for (key, value) in walk(file2))
    keys1 = set(content1.keys())
    keys2 = set(content2.keys())

    all_keys = sorted(keys1 | keys2)

    for name in all_keys:
        comparison[name] = {}
        status = FAILED
        evaluationValue, ks_statistic, pvalue = 0, 0, 0
        diff = np.array([])
        reason = ''

        evaluationFunc = maxRelativeDifference
        cut = 'value <= {}'.format(tolerance)

        value1, value2 = load_values(name, content1, content2)

        if len(value1) == 0 and len(value2) == 0:
            status = SUCCESS
            pvalue = 1
        elif (len(value1) == 0 and len(value2) > 0) or (len(value1) > 0 and len(value2) == 0):
            status = FAILED
            reason = 'file1 is empty' if len(value1) > 0 else 'reference file is empty'
            diff = value1 if len(value1) > 0 else value2
        else:
            ks_statistic, pvalue = stats.ks_2samp(value2, value1)

            try:
                diff = difference(value2, value1)
                evaluationValue = evaluationFunc(value1, value2)
                status = evaluateStatus(value1, value2, evaluationFunc, cut)
            except Exception as e:
                reason = str(e)
                status = UNKNOWN

        comparison[name] = dict(
            status=status,
            original=value1,
            reference=value2,
            diff=diff,
            evaluationValue=evaluationValue,
            ks_statistic=ks_statistic,
            pvalue=pvalue,
            reason=reason,
        )
    return comparison


def load_values(name, content1, content2):
    value1 = content1[name] if name in content1 else np.array([])
    value2 = content2[name] if name in content2 else np.array([])
    value1 = np.array(value1)
    value2 = np.array(value2)

    # if len(value1) == 0 and len(value2) == 0:

    dimension = max(np.ndim(value1), np.ndim(value2))
    if dimension > 1:
        value1 = value1.flatten()
        value2 = value2.flatten()
    return value1, value2


def evaluateStatus(value1, value2, evaluationFunc, cut):
    status = FAILED
    if is_ok(evaluationFunc, cut=cut, value1=value1, value2=value2):
        status = SUCCESS
    return status


def maxRelativeDifference(value1, value2, normalisation=None):
    diff = difference(value2, value1)
    d = np.absolute(diff)
    if normalisation is None:
        normalisation = np.sqrt(np.sum(value2**2))

    if abs(normalisation) == np.Infinity or np.Infinity in d:
        return np.Infinity
    if normalisation == 0:
        return 0

    return max(d / normalisation)


__all__ = [
    'absolute_to_relative_timestamps',
    'compare_metrics',
    'compare_two_root_files',
]

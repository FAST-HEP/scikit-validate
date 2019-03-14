from __future__ import division
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


def is_ok(diff, normalisation, tolerance=0.02):
    d = np.absolute(diff)

    if abs(normalisation) == np.Infinity or np.Infinity in d:
        return False
    if normalisation == 0:
        return True

    return max(d / normalisation) <= tolerance


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
        value1 = content1[name] if name in content1 else np.array([np.Infinity])
        value2 = content2[name] if name in content2 else np.array([np.Infinity])

        diff = difference(value2, value1)
        status = FAILED
        ks_statistic, pvalue = stats.ks_2samp(value2, value1)

        if not len(diff):
            status = UNKNOWN
        else:
            norm = np.sqrt(np.sum(value2**2))
            if is_ok(diff, normalisation=norm, tolerance=tolerance):
                status = SUCCESS

        comparison[name] = dict(
            status=status,
            original=value1,
            reference=value2,
            diff=diff,
            ks_statistic=ks_statistic,
            pvalue=pvalue,
        )
    return comparison


__all__ = [
    'absolute_to_relative_timestamps',
    'compare_metrics',
    'compare_two_root_files',
]

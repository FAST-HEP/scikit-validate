from __future__ import division
import numpy as np
from skvalidate.io import walk


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
    are_OK = []
    are_not_OK = []

    content1 = dict((key, value) for (key, value) in walk(file1))
    content2 = dict((key, value) for (key, value) in walk(file2))
    keys1 = set(content1.keys())
    keys2 = set(content2.keys())

    allKeys = sorted(keys1 | keys2)

    for name in allKeys:
        value1 = content1[name] if name in content1 else np.array([np.Infinity])
        value2 = content2[name] if name in content2 else np.array([np.Infinity])

        diff = difference(value2, value1)
        if not len(diff):
            are_not_OK.append((name, (value1, value2, diff)))
            continue
        norm = np.sqrt(np.sum(value2**2))
        if not is_ok(diff, normalisation=norm, tolerance=tolerance):
            are_not_OK.append((name, (value1, value2, diff)))
        else:
            are_OK.append((name, (value1, value2, diff)))
    return are_OK, are_not_OK

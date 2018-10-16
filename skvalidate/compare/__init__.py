import numpy as np


def difference(a1, a2):
    try:
        return a1 - a2
    except Exception:
        # TODO: need to compare string as well?
        return [0]


def is_ok(diff, normalisation=np.linalg.norm, tolerance=0.02):
    d = np.absolute(diff)
    norm = normalisation(d)
    if norm == 0:
        return True

    return max(d / norm) <= tolerance

from __future__ import division
import numpy as np
import pytest
from skvalidate.compare import compare_two_root_files, difference, is_ok, maxRelativeDifference
import skvalidate.compare as skcmp


@pytest.mark.parametrize("a1,a2,expected", [
    (
        np.array([1, 2, 3]),
        np.array([1, 2, 3]),
        np.array([0, 0, 0]),
    ),
    (
        np.array([1, 2, 3]),
        np.array([-1, -2, -3]),
        np.array([2, 4, 6]),
    ),
    (
        np.array(['1', '2', '3']),
        np.array(['1', '2', '3']),
        np.array([]),
    ),
])
def test_difference(a1, a2, expected):
    result = difference(a1, a2)
    assert np.array_equal(result, expected)


@pytest.mark.parametrize("value1,value2,normalisation,tolerance,expected", [
    (
        np.array([0, 0, 0]),
        np.array([0, 0, 0]),
        1,
        0,
        True
    ),
    (
        np.array([1, 2, 3]),
        np.array([2, 4, 6]),
        1,
        0,
        False
    ),
    (
        np.array([1, 2, 3]),
        np.array([2, 4, 6]),
        6,
        0.1,
        False
    ),
    (
        np.array([1, 2, 3]),
        np.array([2, 4, 6]),
        50,
        0.1,
        True
    ),
    (
        np.array([1, 2, 3]),
        np.array([2, 4, 6]),
        np.Infinity,
        0.1,
        False
    ),
    (
        np.array([np.Infinity, np.Infinity, np.Infinity]),
        np.array([2, 4, 6]),
        1,
        0.02,
        False
    ),
    (
        np.array([np.Infinity, np.Infinity, np.Infinity]),
        np.array([2, 4, 6]),
        np.Infinity,
        0.1,
        False
    ),
    (
        np.array([np.Infinity, np.Infinity, np.Infinity]),
        np.array([2, 4, 6]),
        0,
        0.1,
        False
    ),
])
def test_is_ok(value1, value2, normalisation, tolerance, expected):
    cut = 'value <= {0}'.format(tolerance)
    assert is_ok(maxRelativeDifference, cut=cut, value1=value1, value2=value2, normalisation=normalisation) == expected


@pytest.mark.parametrize("value1,value2,normalisation,expected", [
    (
        np.array([0, 0, 0]),
        np.array([0, 0, 0]),
        None,
        0
    ),
    (
        np.array([1, 2, 3]),
        np.array([2, 4, 6]),
        1,
        3,
    ),
    (
        np.array([1, 2, 3]),
        np.array([2, 4, 6]),
        6,
        3 / 6,
    ),
    (
        np.array([1, 2, 3]),
        np.array([2, 4, 6]),
        50,
        3 / 50,
    ),
    (
        np.array([1, 2, 3]),
        np.array([2, 4, 6]),
        np.Infinity,
        np.Infinity
    ),
    (
        np.array([np.Infinity, np.Infinity, np.Infinity]),
        np.array([2, 4, 6]),
        1,
        np.Infinity,
    ),
    (
        np.array([np.Infinity, np.Infinity, np.Infinity]),
        np.array([2, 4, 6]),
        np.Infinity,
        np.Infinity,
    ),
    (
        np.array([np.Infinity, np.Infinity, np.Infinity]),
        np.array([2, 4, 6]),
        0,
        np.Infinity,
    ),
])
def test_maxRelativeDifference(value1, value2, normalisation, expected):
    assert maxRelativeDifference(value1, value2, normalisation) == expected


@pytest.mark.parametrize("file1,file2,tolerance,n_ok,n_not_ok", [
    (
        'tests/samples/test_1.root',
        'tests/samples/test_1.root',
        0,
        5,
        0
    ),
    (
        'tests/samples/test_1.root',
        'tests/samples/test_2.root',
        0.02,
        2,
        3
    ),
    (
        'tests/samples/test_1.root',
        'tests/samples/test_2.root',
        1,
        5,
        0
    ),
    (
        'tests/samples/test_1.root',
        'tests/samples/test_3.root',
        0.02,
        2,
        4
    ),
    (
        'tests/samples/test_3.root',
        'tests/samples/test_1.root',
        0.02,
        2,
        4
    ),
    (
        'tests/samples/objects.root',
        'tests/samples/objects.root',
        0.02,
        11,
        0
    ),
])
def test_compare_two_root_files(file1, file2, tolerance, n_ok, n_not_ok):
    comparison = compare_two_root_files(file1, file2, tolerance=tolerance)
    n_cmp_ok = sum([v['status'] == skcmp.SUCCESS for v in comparison.values()])
    n_cmp_not_ok = len(comparison) - n_cmp_ok
    assert n_cmp_ok == n_ok
    assert n_cmp_not_ok == n_not_ok

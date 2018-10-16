import numpy as np
import pytest

from skvalidate.compare import compare_two_root_files, difference, is_ok


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
        np.array([0]),
    ),
])
def test_difference(a1, a2, expected):
    result = difference(a1, a2)
    assert np.array_equal(result, expected)


@pytest.mark.parametrize("diff,normalisation,tolerance,expected", [
    (
        np.array([0, 0, 0]),
        1,
        0,
        True
    ),
    (
        np.array([1, 2, 3]),
        1,
        0,
        False
    ),
    (
        np.array([1, 2, 3]),
        6,
        0.1,
        False
    ),
    (
        np.array([1, 2, 3]),
        50,
        0.1,
        True
    ),
    (
        np.array([1, 2, 3]),
        np.Infinity,
        0.1,
        False
    ),
    (
        np.array([np.Infinity, np.Infinity, np.Infinity]),
        1,
        0.02,
        False
    ),
    (
        np.array([np.Infinity, np.Infinity, np.Infinity]),
        np.Infinity,
        0.1,
        False
    ),
    (
        np.array([np.Infinity, np.Infinity, np.Infinity]),
        0,
        0.1,
        False
    ),
])
def test_is_ok(diff, normalisation, tolerance, expected):
    assert is_ok(diff, normalisation, tolerance=tolerance) == expected


@pytest.mark.parametrize("file1,file2,tolerance,nOK,nNotOK", [
    (
        'tests/samples/test_1.root',
        'tests/samples/test_1.root',
        0,
        4,
        0
    ),
    (
        'tests/samples/test_1.root',
        'tests/samples/test_2.root',
        0.02,
        1,
        3
    ),
    (
        'tests/samples/test_1.root',
        'tests/samples/test_2.root',
        1,
        4,
        0
    ),
    (
        'tests/samples/test_1.root',
        'tests/samples/test_3.root',
        0.02,
        1,
        4
    ),
    (
        'tests/samples/test_3.root',
        'tests/samples/test_1.root',
        0.02,
        1,
        4
    ),
])
def test_compare_two_root_files(file1, file2, tolerance, nOK, nNotOK):
    ok, notOK = compare_two_root_files(file1, file2, tolerance=tolerance)
    assert len(ok) == nOK
    assert len(notOK) == nNotOK

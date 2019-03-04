import os
import pytest

from skvalidate.io import resolve_wildcard_path

test_1_file = os.path.join('tests', 'samples', 'test_1.root')
test_2_file = os.path.join('tests', 'samples', 'test_2.root')
test_3_file = os.path.join('tests', 'samples', 'test_3.root')
test_files = [os.path.abspath(p) for p in [test_1_file, test_2_file, test_3_file]]
test_1_file, test_2_file, test_3_file = test_files

@pytest.mark.parametrize('wildcard_path,expected', [
    (
        'tests/samples/test_1.root',
        [test_1_file],
    ),
    (
        'tests/samples/test_*.root',
        test_files,
    ),
])
def test_resolve_wildcard_path(wildcard_path, expected):
    result = list(resolve_wildcard_path(wildcard_path))
    assert len(result) == len(expected)
    assert sorted(result) == sorted(expected)

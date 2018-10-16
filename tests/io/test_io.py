import numpy as np
import pytest
from skvalidate.io import walk


@pytest.mark.parametrize("input_file,names,types", [
    (
        'tests/samples/test_1.root',
        ['test;1.i', 'test;1.x', 'test;1.y', 'test;1.z'],
        [np.int32, np.float32, np.float32, np.float32]
    ),
    (
        'tests/samples/test_2.root',
        ['test;1.i', 'test;1.x', 'test;1.y', 'test;1.z'],
        [np.int32, np.float32, np.float32, np.float32]
    ),
    (
        'tests/samples/test_3.root',
        ['test;1.i', 'test;1.x', 'test;1.y', 'test;1.z', 'test;1.a'],
        [np.int32, np.float32, np.float32, np.float32, np.float32]
    ),
])
def test_walk(input_file, names, types):
    result = list(walk(input_file))

    for name, array in result:
        assert name in names
        assert array.dtype == types[names.index(name)]

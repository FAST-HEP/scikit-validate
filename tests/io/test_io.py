import numpy as np
from skvalidate.io import walk


def test_walk():
    result = list(walk('tests/samples/test_1.root'))
    keys = ['test;1.i',  'test;1.x', 'test;1.y', 'test;1.z']
    types = [np.int32, np.float32, np.float32, np.float32]
    for i, k, t in zip(result, keys, types):
        name, array = i
        assert name == k
        assert array.dtype == t

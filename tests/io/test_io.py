import numpy as np
import pytest
from skvalidate.io import walk
import skvalidate.io as skio


@pytest.mark.parametrize('input_file,names,types,unpack_fields', [
    (
        'tests/samples/test_1.root',
        ['test;1.i', 'test;1.x', 'test;1.y', 'test;1.z', 'test;1.v', 'test;1.string'],
        [np.int32, np.float32, np.float32, np.float32, np.float32, np.object_],
        False,
    ),
    (
        'tests/samples/test_2.root',
        ['test;1.i', 'test;1.x', 'test;1.y', 'test;1.z', 'test;1.v', 'test;1.string'],
        [np.int32, np.float32, np.float32, np.float32, np.float32, np.object_],
        False,
    ),
    (
        'tests/samples/test_3.root',
        ['test;1.i', 'test;1.x', 'test;1.y', 'test;1.z', 'test;1.v', 'test;1.a'],
        [np.int32, np.float32, np.float32, np.float32, np.float32, np.float32],
        False,
    ),
    (
        'tests/samples/objects.root',
        [
            'Events;1.MyEvent.TObject.fBits',
            'Events;1.MyEvent.TObject.fUniqueID',
            'Events;1.MyEvent.eventID',
            'Events;1.MyEvent.ayes.end_ns',
            'Events;1.MyEvent.ayes.start_ns',
            'Events;1.MyEvent.bees.driftTime',
            'Events;1.MyEvent.bees.xyPosition',
            'Events;1.MyEvent.bees.xyzPosition',
        ],
        [
            np.uint32, np.uint32, np.uint32,
            np.float32, np.float32,
            np.float32,
            np.float64, np.float64,
            np.float64, np.float64, np.float64
        ],
        False,
    ),
    (
        'tests/samples/objects.root',
        [
            'Events;1.MyEvent.TObject.fBits',
            'Events;1.MyEvent.TObject.fUniqueID',
            'Events;1.MyEvent.eventID',
            'Events;1.MyEvent.ayes.end_ns',
            'Events;1.MyEvent.ayes.start_ns',
            'Events;1.MyEvent.bees.driftTime',
            'Events;1.MyEvent.bees.xyPosition.fX',
            'Events;1.MyEvent.bees.xyPosition.fY',
            'Events;1.MyEvent.bees.xyzPosition.fX',
            'Events;1.MyEvent.bees.xyzPosition.fY',
            'Events;1.MyEvent.bees.xyzPosition.fZ',
        ],
        [
            np.uint32, np.uint32, np.uint32,
            np.float32, np.float32,
            np.float32,
            np.float64, np.float64,
            np.float64, np.float64, np.float64
        ],
        True,
    ),
    (
        'tests/samples/non_tree_objects.root',
        ['1Dhist;1', '2Dhist;1'],
        [np.int32, np.float32],
        False,
    ),
])
def test_walk(input_file, names, types, unpack_fields):
    result = list(walk(input_file, unpack_fields))
    assert len(result) == len(names)

    for name, array in result:
        assert name in names
        if hasattr(array, 'dtype'):
            assert array.dtype == types[names.index(name)]


@pytest.mark.parametrize('input_file,expected_len', [
    ('tests/samples/objects.root', 1000),
    ('tests/samples/test_1.root', 10000),
    ('tests/samples/test_3.root', 10000),
])
def test_load_array(input_file, expected_len):
    file_keys = skio.recursive_keys(input_file)
    for array_name in file_keys:
        array = skio.load_array(input_file, array_name)
        assert array is not None
        assert len(array) == expected_len


def test_load_array_from_object():
    input_file = 'tests/samples/objects.root'
    array_names = [
        'Events;1.MyEvent.bees.xyzPosition.fX',
        'Events;1.MyEvent.bees.xyzPosition.fY',
        'Events;1.MyEvent.bees.xyzPosition.fZ',
    ]
    for array_name in array_names:
        tokens = array_name.split('.')
        obj_path = '.'.join(tokens[:-1])
        var = tokens[-1]
        array = skio.load_array(input_file, array_name)
        array2 = skio.load_array(input_file, obj_path)
        assert array is not None
        assert len(array) == 1000
        assert np.all(array == array2[var])

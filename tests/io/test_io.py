import numpy as np
import pytest
from skvalidate.io import walk


@pytest.mark.parametrize('input_file,names,types', [
    (
        'tests/samples/test_1.root',
        ['test;1.i', 'test;1.x', 'test;1.y', 'test;1.z', 'test;1.v'],
        [np.int32, np.float32, np.float32, np.float32, np.float32]
    ),
    (
        'tests/samples/test_2.root',
        ['test;1.i', 'test;1.x', 'test;1.y', 'test;1.z', 'test;1.v'],
        [np.int32, np.float32, np.float32, np.float32, np.float32]
    ),
    (
        'tests/samples/test_3.root',
        ['test;1.i', 'test;1.x', 'test;1.y', 'test;1.z', 'test;1.v', 'test;1.a'],
        [np.int32, np.float32, np.float32, np.float32, np.float32, np.float32]
    ),
    (
        'tests/samples/objects.root',
        [
            'Events;1.MyEvent.TObject.fUniqueID', 'Events;1.MyEvent.TObject.fBits', 'Events;1.MyEvent.eventID',
            'Events;1.MyEvent.ayes.start_ns', 'Events;1.MyEvent.ayes.end_ns',
            'Events;1.MyEvent.bees.driftTime',
            'Events;1.MyEvent.bees.xyPosition._fX', 'Events;1.MyEvent.bees.xyPosition._fY',
            'Events;1.MyEvent.bees.xyzPosition._fX', 'Events;1.MyEvent.bees.xyzPosition._fY',
            'Events;1.MyEvent.bees.xyzPosition._fZ',
        ],
        [
            np.uint32, np.uint32, np.uint32,
            np.float32, np.float32,
            np.float32,
            np.float64, np.float64,
            np.float64, np.float64, np.float64
        ]
    ),
])
def test_walk(input_file, names, types):
    result = list(walk(input_file))
    assert len(result) == len(names)

    for name, array in result:
        assert name in names
        assert array.dtype == types[names.index(name)]

import awkward as ak
import numpy as np

from skvalidate.operations._awkward import unpack, unpack_array


def __test_sub_arrays(object_type_ak_array, sub_arrays):
    assert 'fX' in sub_arrays
    assert 'fY' in sub_arrays
    assert len(sub_arrays) == 2
    assert len(sub_arrays['fX']) == len(sub_arrays['fY']) \
        and len(sub_arrays['fX']) == len(object_type_ak_array)
    assert np.all(sub_arrays['fX'] == object_type_ak_array.fX)
    assert np.all(sub_arrays['fY'] == object_type_ak_array.fY)


def test_object_unpack(object_type, object_type_ak_array):
    sub_arrays = unpack(object_type)
    __test_sub_arrays(object_type_ak_array, sub_arrays)


def test_object_unpack_array(object_type_ak_array):
    sub_arrays = unpack_array(object_type_ak_array)
    __test_sub_arrays(object_type_ak_array, sub_arrays)


def test_array_unpack():
    array = ak.Array([[3.3, 2.2, 1.1], [], [4.4, 5.5]])
    sub_arrays_from_unpack = unpack(array)
    sub_arrays = unpack_array(array)

    assert np.all(sub_arrays == array)
    assert np.all(sub_arrays_from_unpack == array)

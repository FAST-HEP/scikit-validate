import awkward as ak
import numpy as np
import pytest

import skvalidate.operations._awkward  # noqa F401


def test_scalar_absolute(scalar_type_ak_array):
    absolute = abs(scalar_type_ak_array)
    ak.to_numpy(absolute) == np.absolute(ak.to_numpy(absolute))


def test_object_absolute(object_type_ak_array):
    absolute = abs(object_type_ak_array)
    ak.to_numpy(absolute) == np.absolute(ak.to_numpy(absolute))


def test_scalar_subtract(scalar_type_ak_array):
    diff = np.subtract(scalar_type_ak_array, scalar_type_ak_array)
    np_array = ak.to_numpy(diff)
    ak.to_numpy(diff) == np.subtract(np_array, np_array)


def test_object_subtract(object_type_ak_array):
    diff = np.subtract(object_type_ak_array, object_type_ak_array)
    np_array = ak.to_numpy(diff)
    ak.to_numpy(diff) == np.subtract(np_array, np_array)


def test_scalar_amax(scalar_type_ak_array):
    amax = ak.max(scalar_type_ak_array, initial=-9000)
    np_array = ak.to_numpy(scalar_type_ak_array)
    amax == np.amax(np_array, initial=-9000)


def test_object_amax(object_type_ak_array):
    amax = np.amax(object_type_ak_array.fX, initial=-9000)
    np_array = ak.to_numpy(object_type_ak_array.fX)
    amax == np.amax(np_array, initial=-9000)


def test_scalar_laNorm(scalar_type_ak_array):
    with pytest.raises(TypeError):
        norm = np.linalg.norm(scalar_type_ak_array)
        np_array = ak.to_numpy(scalar_type_ak_array)
        norm == np.linalg.norm(np_array)


def test_object_laNorm(object_type_ak_array):
    with pytest.raises(TypeError):
        norm = np.linalg.norm(object_type_ak_array)
        np_array = ak.to_numpy(object_type_ak_array)
        norm == np.linalg.norm(np_array)


def test_scalar_sum(scalar_type_ak_array):
    theSum = np.sum(scalar_type_ak_array)
    np_array = ak.to_numpy(theSum)
    ak.to_numpy(theSum) == np.sum(np_array)


def test_object_sum(object_type_ak_array):
    theSum = np.sum(object_type_ak_array)
    np_array = ak.to_numpy(theSum)
    ak.to_numpy(theSum) == np.sum(np_array)

# amax, linalg.norm

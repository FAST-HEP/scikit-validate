import awkward as ak
import numpy as np

ak.behavior[np.absolute, "TVector2"] = lambda data: np.sqrt(data.fX**2 + data.fY**2)
ak.behavior[np.subtract, "TVector2", "TVector2"] = lambda left, right: np.sqrt(
    (left.fX - right.fX)**2 + (left.fY - right.fY)**2)

ak.behavior[np.absolute, "TVector3"] = lambda data: np.sqrt(data.fX**2 + data.fY**2 + data.fZ**2)
ak.behavior[np.subtract, "TVector3", "TVector3"] = lambda left, right: np.sqrt(
    (left.fX - right.fX)**2 + (left.fY - right.fY)**2 + (left.fZ - right.fZ)**2)

ak.behavior[np.linalg.norm, "TVector2"] = lambda data: np.sqrt(np.sum(abs(data * data)))
ak.behavior[np.linalg.norm, "TVector3"] = lambda data: np.sqrt(np.sum(abs(data * data)))

ak.behavior[np.multiply, "TVector2", "TVector2"] = lambda left, right: left.fX * \
    right.fX + left.fY * right.fY
ak.behavior[np.multiply, "TVector3", "TVector3"] = lambda left, right: left.fX * \
    right.fX + left.fY * right.fY + left.fZ * right.fZ


def parse_fields(array):
    layout = array.layout
    return layout.keys()


def unpack(obj):
    if not hasattr(obj, 'array'):
        return obj
    return unpack_array(obj.array())

def unpack_array(array):
    fields = parse_fields(array)
    if fields:
        return {f: getattr(array, f) for f in fields}
    return array

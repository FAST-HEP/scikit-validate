from hypothesis import given, assume
import hypothesis.strategies as st
import pytest
import numpy as np

from skvalidate.vis import adjust_axis_limits, draw_diff, find_limits


@given(st.floats(min_value=-1e6, max_value=1e6), st.floats(min_value=-1e6, max_value=1e6))
def test_positive_change_adjust_axis_limits(a_min, a_max):
    assume(a_max > a_min)
    logy = False
    change = 0.2
    new_a_min, new_a_max = adjust_axis_limits(a_min, a_max, change, logy)

    assert new_a_min < a_min if a_min != 0 else new_a_min == a_min
    assert new_a_max > a_max if a_max != 0 else new_a_max == a_max


@given(st.floats(min_value=-1e6, max_value=1e6), st.floats(min_value=-1e6, max_value=1e6))
def test_negative_change_adjust_axis_limits(a_min, a_max):
    assume(a_max > a_min)
    logy = False
    change = - 0.2
    new_a_min, new_a_max = adjust_axis_limits(a_min, a_max, change, logy)

    assert new_a_min > a_min if a_min != 0 else new_a_min == a_min
    assert new_a_max < a_max if a_max != 0 else new_a_max == a_max


@given(st.floats(min_value=-1e6, max_value=1e6), st.floats(min_value=-1e6, max_value=1e6))
def test_logy_adjust_axis_limits(a_min, a_max):
    assume(a_max > a_min)
    assume(a_max > 0)
    logy = True
    change = 0.2
    new_a_min, new_a_max = adjust_axis_limits(a_min, a_max, change, logy)

    assert new_a_min > 0
    assert new_a_max > 0
    assert new_a_min < a_min if a_min > 0 else new_a_min > 0
    assert new_a_max > a_max if a_max > 0 else new_a_max > 0


@given(st.text(), st.text())
def _test_string_adjust_axis_limits(a_min, a_max):
    logy = False
    change = 0.2
    pytest.raises(TypeError, adjust_axis_limits(a_min, a_max, change, logy))


@pytest.mark.parametrize('original,reference,amin,amax', [
    (
        np.array([1, 2, 3, 4]),
        np.array([1, 3, 4, 5]),
        1,
        5,
    ),
    (
        np.array([1, 2, 3, 4]),
        None,
        1,
        4,
    ),
    (
        np.array([1, 2, 3, 4]),
        [],
        1,
        4,
    ),
])
def test_find_limits(original, reference, amin, amax):
    l1, l2 = find_limits(original, reference)
    assert l1 == amin
    assert l2 == amax


@pytest.mark.parametrize('original,reference,', [
    (
        np.array([1, 2, 3, 4]),
        np.array([1, 3, 4, 5]),
    ),
    (
        np.array([1, 2, 3, 4]),
        None,
    ),
    (
        np.array([1, 2, 3, 4]),
        [],
    ),
])
def test_draw_diff(original, reference):
    name = 'test123'
    output_path = '/tmp'
    values = {
        'original': original,
        'reference': reference,
        'ks_statistic': 0,
        'pvalue': 0,
    }
    draw_diff(name, values, output_path)

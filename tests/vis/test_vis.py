from hypothesis import given, assume
import hypothesis.strategies as st
import pytest

from skvalidate.vis import adjust_axis_limits


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

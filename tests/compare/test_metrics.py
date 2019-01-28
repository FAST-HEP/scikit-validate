import pytest
from skvalidate.compare.metrics import convert_old_to_new

old_to_new = (
    {
        "file1": {
            "size_in_bytes": 84890132,
        }
    },
    {
        "file1": {
            "size_in_bytes": {
                'value': 84890132,
                'unit': ''
            },
        }
    },
)

new_to_new = (
    {
        "file1": {
            "size_in_bytes": {
                'value': 84890132,
                'unit': 'B'
            },
        }
    },
    {
        "file1": {
            "size_in_bytes": {
                'value': 84890132,
                'unit': 'B'
            },
        }
    },
)

broken_new_to_new = (
    {
        "file1": {
            "size_in_bytes": {
                'value': 84890132,
            },
        }
    },
    {
        "file1": {
            "size_in_bytes": {
                'value': 84890132,
                'unit': ''
            },
        }
    },
)


@pytest.mark.parametrize("old_style,new_style", [
    old_to_new,
    new_to_new,
    broken_new_to_new,
])
def test_conversion_old_to_new(old_style, new_style):
    converted = convert_old_to_new(old_style)
    assert converted == new_style

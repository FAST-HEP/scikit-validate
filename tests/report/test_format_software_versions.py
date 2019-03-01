import pytest
from skvalidate.report import format_software_versions


@pytest.mark.parametrize('items,expected', [
    (
        dict(
            job_1=dict(
                software_versions=dict(job_1={'python': '2.7.15', 'root': '6.16.00'}),
                other={},
            ),
            job_2=dict(
                software_versions=dict(job_2={'python': '3.6.5', 'root': '6.16.00'}),
                other={},
            ),
        ),
        dict(
            job_1=['python=2.7.15', 'root=6.16.00'],
            job_2=['python=3.6.5', 'root=6.16.00'],
        )
    ),
])
def test_format_software_versions(items, expected):
    result = format_software_versions(items)
    assert len(result) == len(items)

    for name, content in result.items():
        assert sorted(content['software_versions']) == sorted(expected[name])

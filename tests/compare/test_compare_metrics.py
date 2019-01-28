from __future__ import division
import pytest
from skvalidate.compare import compare_metrics

file_metrics = (
    {
        "file1": {
            "size_in_bytes": {'value': 84890132, 'unit': 'B'},
            "size_in_mb": {'value': 81.0, 'unit': 'MB'},
        },
        "file2": {
            "size_in_bytes": {'value': 14951803, 'unit': 'B'},
            "size_in_mb": {'value': 14.3, 'unit': 'MB'}},
    },
    {
        "file1": {
            "size_in_bytes": {'value': 41487008, 'unit': 'B'},
            "size_in_mb": {'value': 39.6, 'unit': 'MB'},
        },
        "file2": {
            "size_in_bytes": {'value': 9857661, 'unit': 'B'},
            "size_in_mb": {'value': 9.4, 'unit': 'MB'}},
    },
    ['size_in_bytes'],
    {
        "file1": {
            'size_in_bytes': {
                'unit': 'B',
                'value': 84890132,
                'ref': 41487008,
                'diff': 84890132 - 41487008,
                'diff_pc': (84890132 - 41487008) / 41487008 * 100,
            },
        },
        "file2": {
            'size_in_bytes': {
                'unit': 'B',
                'value': 14951803,
                'ref': 9857661,
                'diff': 14951803 - 9857661,
                'diff_pc': (14951803 - 9857661) / 9857661 * 100,
            },
        }
    }
)

missing_ref = (
    {
        'cmd1': {
            'walltime': {'value': 1000},
            'memory_in_gb': {'value': 2.1},
        },
        'cmd2': {
            'walltime': {'value': 500},
            'memory_in_gb': {'value': 1.1},
        }
    },
    {
        'cmd1': {
            'walltime': {'value': 1000},
        }
    },
    None,
    {
        "cmd1": {
            'walltime': {
                'unit': '',
                'value': 1000,
                'ref': 1000,
                'diff': 0,
                'diff_pc': 0,
            },
            'memory_in_gb': {
                'unit': '',
                'value': 84890132,
                'ref': '---',
                'diff': '---',
                'diff_pc': '---',
            },
        },
        "cmd2": {
            'walltime': {
                'unit': '',
                'value': 500,
                'ref': '---',
                'diff': '---',
                'diff_pc': '---',
            },
            'memory_in_gb': {
                'unit': '',
                'value': '---',
                'ref': '---',
                'diff': '---',
                'diff_pc': '---',
            },
        }
    }

)

old_style_metrics = (
    {
        "file1": {
            "size_in_bytes": {'value': 84890132, 'unit': 'B'},
            "size_in_mb": {'value': 81.0, 'unit': 'MB'},
        },
        "file2": {
            "size_in_bytes": {'value': 14951803, 'unit': 'B'},
            "size_in_mb": {'value': 14.3, 'unit': 'MB'}},
    },
    {
        "file1": {
            "size_in_bytes": 41487008,
            "size_in_mb": 39.6,
        },
        "file2": {
            "size_in_bytes": 9857661,
            "size_in_mb": 9.4,
        },
    },
    ['size_in_bytes'],
    {
        "file1": {
            'size_in_bytes': {
                'unit': 'B',
                'value': 84890132,
                'ref': 41487008,
                'diff': 84890132 - 41487008,
                'diff_pc': (84890132 - 41487008) / 41487008 * 100,
            },
        },
        "file2": {
            'size_in_bytes': {
                'unit': 'B',
                'value': 14951803,
                'ref': 9857661,
                'diff': 14951803 - 9857661,
                'diff_pc': (14951803 - 9857661) / 9857661 * 100,
            },
        }
    }
)

@pytest.mark.parametrize("metrics,metrics_ref,keys,diff", [
    file_metrics,
    missing_ref,
    old_style_metrics,
])  # TODO: add with keys=None
def test_compare_file_metrics(metrics, metrics_ref, keys, diff):
    result = compare_metrics(metrics, metrics_ref, keys=keys)
    if keys is None:
        keys = set(list(metrics.keys()) + list(metrics_ref.keys()))
    diff_keys = ['diff', 'diff_pc', 'ref', 'value', 'unit']
    for name, comparison in result.items():
        for m_name, metric in comparison.items():
            assert sorted(metric.keys()) == sorted(diff_keys)
            for k in metric.keys():
                assert metric[k] == diff[name][m_name][k]

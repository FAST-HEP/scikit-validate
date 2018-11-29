import pytest
from skvalidate.commands.execute_with_metrics import print_metrics


@pytest.mark.parametrize('metrics,command', [
    (
        {'sleep 2':
         {
             'cpu_time_in_s': 23,
             'max_rss_in_mb': 200,
         }
         },
        'sleep 2'
    ),
])
def test_print_metrics(capsys, metrics, command):
    msg = [
        '>>> Ran command: "{command}"',
        '>>> in {cpu_time_in_s}s and used {max_rss_in_mb} MB of memory.'
    ]
    msg = '\n'.join(msg)
    expected = msg.format(
        command=command,
        cpu_time_in_s=metrics[command]['cpu_time_in_s'],
        max_rss_in_mb=metrics[command]['max_rss_in_mb'],
    )
    print_metrics(metrics, command)
    captured = capsys.readouterr()
    assert captured.out == expected + '\n'

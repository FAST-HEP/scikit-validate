import pytest
from skvalidate.commands.execute import print_metrics


@pytest.mark.parametrize('metrics,command', [
    (
        {'sleep 2':
         {
             'cpu_time': {
                 'value': 23,
                 'unit': 's',
             },
             'max_rss': {
                 'value': 200,
                 'unit': 'MB',
             }
         }
         },
        'sleep 2'
    ),
])
def test_print_metrics(capsys, metrics, command):
    msg = [
        '>>> Ran command: "{0}"',
        '>>> in {1}{2} and used {3} {4} of memory.'
    ]
    msg = '\n'.join(msg)
    expected = msg.format(
        command,
        metrics[command]['cpu_time']['value'],
        metrics[command]['cpu_time']['unit'],
        metrics[command]['max_rss']['value'],
        metrics[command]['max_rss']['unit'],
    )
    print_metrics(metrics, command)
    captured = capsys.readouterr()
    assert captured.out == expected + '\n'

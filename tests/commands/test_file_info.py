import pytest
from skvalidate.commands.file_info import print_metrics


@pytest.mark.parametrize('metrics,input_file', [
    (
        {'file1':
         {
             'size_in_mb': {
                 'value': 23,
                 'unit': 'MB',
             },
             'size_in_bytes': {
                 'value': 23 * 1024 * 1024,
                 'unit': 'B',
             }
         }
         },
        'file1'
    ),
])
def test_print_metrics(capsys, metrics, input_file):
    msg = [
        '>>> Input file: "{0}"',
        '>>> File size: {1} {2} ({3} {4})'
    ]
    msg = '\n'.join(msg)
    expected = msg.format(
        input_file,
        metrics[input_file]['size_in_mb']['value'],
        metrics[input_file]['size_in_mb']['unit'],
        metrics[input_file]['size_in_bytes']['value'],
        metrics[input_file]['size_in_bytes']['unit'],
    )
    print_metrics(metrics, input_file)
    captured = capsys.readouterr()
    assert captured.out == expected + '\n'

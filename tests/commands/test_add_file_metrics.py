import pytest
from skvalidate.commands.add_file_metrics import print_metrics


@pytest.mark.parametrize('metrics,input_file', [
    (
        {'file1':
         {
             'size_in_mb': 23,
             'size_in_bytes': 23 * 1024 * 1024,
         }
         },
        'file1'
    ),
])
def test_print_metrics(capsys, metrics, input_file):
    msg = [
        '>>> Input file: "{input_file}"',
        '>>> File size: {size_in_mb} MB ({size_in_bytes} bytes)'
    ]
    msg = '\n'.join(msg)
    expected = msg.format(
        input_file=input_file,
        size_in_mb=metrics[input_file]['size_in_mb'],
        size_in_bytes=metrics[input_file]['size_in_bytes'],
    )
    print_metrics(metrics, input_file)
    captured = capsys.readouterr()
    assert captured.out == expected + '\n'

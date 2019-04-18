"""
Script to record file metrics.

For testing pick or create a file:

:Example:

 .. code-block:: bash

    # create 10 MB file
    dd if=/dev/zero of=test.file bs=10485760 count=1
    sv_file_info test.file -m file_metrics.json

If the output file, default ``file_metrics.json``, already exists it will be read first and results will be appended.
"""
from __future__ import division, print_function

import os

import click

from skvalidate.io import save_metrics_to_file


def get_file_metrics(input_file):
    statinfo = os.stat(input_file)
    size_in_bytes = statinfo.st_size
    size_in_mb = size_in_bytes / 1024 / 1024
    metrics = dict(
        size_in_bytes=dict(
            value=size_in_bytes,
            unit='B',
            lower_is_better=True,
        ),
        size_in_mb=dict(
            value=round(size_in_mb, 1),
            unit='MB',
            lower_is_better=True,
        ),
    )
    metrics = {input_file: metrics}
    return metrics


def print_metrics(metrics, input_file):
    params = dict(input_file=input_file)
    params.update(metrics[input_file])
    msg = [
        '>>> Input file: "{0}"',
        '>>> File size: {1} {2} ({3} {4})'
    ]
    msg = '\n'.join(msg)
    print(msg.format(
        params['input_file'],
        params['size_in_mb']['value'],
        params['size_in_mb']['unit'],
        params['size_in_bytes']['value'],
        params['size_in_bytes']['unit'],
    ))


# TODO: add verbose option
@click.command(help=__doc__)
@click.argument('input_files', type=click.Path(exists=True), nargs=-1)
@click.option('-m', '--metrics-file', default='file_metrics.json', help='file for JSON output')
def cli(input_files, metrics_file):
    metrics = {}
    for input_file in input_files:
        # print(get_file_metrics(input_file))
        file_metrics = get_file_metrics(input_file)
        metrics.update(file_metrics)
        print_metrics(file_metrics, input_file)
    save_metrics_to_file(metrics, metrics_file)

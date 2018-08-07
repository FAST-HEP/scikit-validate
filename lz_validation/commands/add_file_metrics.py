"""
Script to record file metrics.

For testing install 'stress' package and run

\n
    dd if=/dev/zero of=test.file bs=10240 count=1
    lz_validation add_file_metrics test.file
"""
from __future__ import division, print_function

import os

import click

from lz_validation.io import save_metrics_to_file


def get_file_metrics(input_file):
    statinfo = os.stat(input_file)
    size_in_mb = statinfo.st_size / 1024 / 1024
    metrics = dict(
        size_in_bytes=statinfo.st_size,
        size_in_mb=round(size_in_mb, 1),
    )
    metrics = {input_file: metrics}
    return metrics


def print_metrics(metrics):
    input_file = metrics.keys()[0]
    params = dict(input_file=input_file)
    params.update(metrics[input_file])
    msg = [
        '>>> Input file: "{input_file}"',
        '>>> File size: {size_in_mb} MB ({size_in_bytes} bytes)'
    ]
    msg = '\n'.join(msg)
    print(msg.format(**params))


@click.command(help=__doc__)
@click.argument('input_files', type=click.Path(exists=True), nargs=-1)
@click.argument('metrics-file', nargs=1)
@click.option('--metrics-file', default='metrics.json')
def cli(input_files, metrics_file):
    metrics = {}
    for input_file in input_files:
        # print(get_file_metrics(input_file))
        file_metrics = get_file_metrics(input_file)
        metrics.update(file_metrics)
        print_metrics(file_metrics)
    save_metrics_to_file(metrics, metrics_file)

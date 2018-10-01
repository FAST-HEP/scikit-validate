#!/usr/bin/env python
"""
Command that wraps and monitors another command.

For testing install 'stress' package and run

\b
    skvalidate execute_with_metrics 'stress --cpu 1 --io 1 --vm 1 --vm-bytes 128M --timeout 10s --verbose' \
                                    -m resource_metrics.json

If the output file, default resource_metrics.json, already exists it will be read first and results will be appended.
"""
from __future__ import print_function

import errno
import logging
import os
import resource
import subprocess

import click

from skvalidate.io import save_metrics_to_file


def monitor_command(command):
    usage_start = resource.getrusage(resource.RUSAGE_CHILDREN)
    for line in execute(command):
        print(line, end="")
    usage_end = resource.getrusage(resource.RUSAGE_CHILDREN)

    max_rss_in_mb = (usage_end.ru_maxrss - usage_start.ru_maxrss) / 1024.
    metrics = dict(
        cpu_time_in_s=usage_end.ru_utime - usage_start.ru_utime,
        max_rss_in_mb=round(max_rss_in_mb, 1),
    )
    metrics = {' '.join(command): metrics}
    return metrics


def execute(cmd):
    exe = which(cmd[0])
    if exe is None:
        logging.error('Could not find executable "{0}"'.format(cmd[0]))
        raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), cmd[0])
    popen = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)


def which(program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)
    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ['PATH'].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file
    return None


def print_metrics(metrics):
    command = metrics.keys()[0]
    params = dict(command=command)
    params.update(metrics[command])
    msg = [
        '>>> Ran command: "{command}"',
        '>>> in {cpu_time_in_s}s and used {max_rss_in_mb} MB of memory.'
    ]
    msg = '\n'.join(msg)
    print(msg.format(**params))


@click.command(help=__doc__)
@click.argument('command')
@click.option('-m', '--metrics-file', default='resource_metrics.json')
def cli(command, metrics_file):
    metrics = monitor_command(command.split())
    print_metrics(metrics)
    save_metrics_to_file(metrics, metrics_file)

#!/usr/bin/env python
"""
Command that wraps and monitors another command.

For testing install 'stress' package and run

 :Example:

 .. code-block:: bash

    sv_execute 'stress --cpu 1 --io 1 --vm 1 --vm-bytes 128M --timeout 10s --verbose' \
                                    -m resource_metrics.json

If the output file, default ``resource_metrics.json``, \
already exists it will be read first and results will be appended.

If a single string argument is provided as the command then it will be split using white-space, however if multiple
arguments are provided then no additional splitting is performed.  In this case though, use `--` before the command
so that options are passed to the command, rather than this script.
"""
from __future__ import print_function

import errno
import logging
import os
import resource
import six.moves._thread as thread
import subprocess

import click
import memory_profiler as mp


from skvalidate.io import save_metrics_to_file


def monitor_command(command, memprof_file, sample_interval):
    usage_start = resource.getrusage(resource.RUSAGE_CHILDREN)
    for line in execute(command, memprof_file, sample_interval):
        print(line, end="")
    usage_end = resource.getrusage(resource.RUSAGE_CHILDREN)

    max_rss_in_mb = (usage_end.ru_maxrss - usage_start.ru_maxrss) / 1024.
    metrics = dict(
        cpu_time=dict(
            value=usage_end.ru_utime - usage_start.ru_utime,
            unit='s',
            lower_is_better=True,
        ),
        max_rss=dict(
            value=round(max_rss_in_mb, 1),
            unit='MB',
            lower_is_better=True,
        )
    )
    metrics = {' '.join(command): metrics}
    return metrics


def execute(cmd, memprof_file, sample_interval):
    """https://stackoverflow.com/questions/4417546/constantly-print-subprocess-output-while-process-is-running"""
    exe = which(cmd[0])
    if exe is None:
        logging.error('Could not find executable "%s"', cmd[0])
        raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), cmd[0])
    popen = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, universal_newlines=True)
    thread.start_new_thread(memory_profile, (' '.join(cmd), popen, memprof_file, sample_interval))
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        if popen.stderr:
            logging.error(popen.stderr.read())
        raise subprocess.CalledProcessError(return_code, cmd)


def memory_profile(cmd, process, memprof_file, sample_interval):
    with open(memprof_file, "a") as f:
        f.write("CMDLINE {0}\n".format(cmd))
        mp.memory_usage(proc=process, interval=sample_interval, timestamps=True, include_children=True, stream=f)


def which(program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)
    fpath, _ = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ['PATH'].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file
    return None


def print_metrics(metrics, command):
    params = dict(command=command)
    params.update(metrics[command])
    msg = [
        '>>> Ran command: "{0}"',
        ">>> in {1}{2} and used {3} {4} of memory."
    ]
    msg = '\n'.join(msg)
    print(msg.format(
        params['command'],
        params['cpu_time']['value'],
        params['cpu_time']['unit'],
        params['max_rss']['value'],
        params['max_rss']['unit'],
    ))


# TODO: check if click can to quargs
# TODO: add verbose option
@click.command(help=__doc__)
@click.argument('command', nargs=-1)
@click.option('-m', '--metrics-file', default='resource_metrics.json', type=click.Path())
@click.option('--memprof-file', default='mprofile.dat', type=click.Path())
@click.option('--sample-interval', default=0.1, type=float, help="Sampling period (in seconds), defaults to 0.1")
def cli(command, metrics_file, memprof_file, sample_interval):
    if len(command) == 1:
        command = command[0].split()
    metrics = monitor_command(command, memprof_file, sample_interval)
    print_metrics(metrics, " ".join(command))
    try:
        save_metrics_to_file(metrics, metrics_file)
    except IOError:
        logging.exception("Could not create metrics file {0}".format(metrics_file))

#!/usr/bin/env python
"""
Command that wraps and monitors another command.

For testing install 'stress' package and run

\b
    sv_execute 'stress --cpu 1 --io 1 --vm 1 --vm-bytes 128M --timeout 10s --verbose' \
                                    -m resource_metrics.json

If the output file, default resource_metrics.json, already exists it will be read first and results will be appended.

If a single string argument is provided as the command then it will be split using white-space, however if multiple
arguments are provided then no additional splitting is performed.  In this case though, use `--` before the command
so that options are passed to the command, rather than this script.
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
        cpu_time_in_s=dict(
            value=usage_end.ru_utime - usage_start.ru_utime,
            unit='s',
            lower_is_better=True,
        ),
        max_rss_in_mb=dict(
            value=round(max_rss_in_mb, 1),
            unit='MB',
            lower_is_better=True,
        )
    )
    metrics = {' '.join(command): metrics}
    return metrics


def execute(cmd):
    """https://stackoverflow.com/questions/4417546/constantly-print-subprocess-output-while-process-is-running"""
    exe = which(cmd[0])
    if exe is None:
        logging.error('Could not find executable "%s"', cmd[0])
        raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), cmd[0])
    popen = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        if popen.stderr:
            logging.error(popen.stderr.read())
        raise subprocess.CalledProcessError(return_code, cmd)


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
        params['cpu_time_in_s']['value'],
        params['cpu_time_in_s']['unit'],
        params['max_rss_in_mb']['value'],
        params['max_rss_in_mb']['unit'],
    ))


# TODO: check if click can to quargs
# TODO: add verbose option
@click.command(help=__doc__)
@click.argument('command', nargs=-1)
@click.option('-m', '--metrics-file', default='resource_metrics.json')
@click.option('--memprof-file', default='mprofile.dat')
def cli(command, metrics_file, memprof_file):
    if len(command) == 1:
        # TODO: Removing this approach so that white-space in the command is
        # handled at the invocation of this script by the actual shell
        command = command[0].split()
    metrics = monitor_command(command)
    print_metrics(metrics, " ".join(command))
    try:
        save_metrics_to_file(metrics, metrics_file)
    except IOError:
        logging.exception("Could not create metrics file '%s'", metrics_file)


# add mprof
# with open(mprofile_output, "a") as f:
#         f.write("CMDLINE {0}\n".format(cmd_line))
#         mp.memory_usage(proc=p, interval=options.interval, timestamps=True,
#                          include_children=options.include_children, stream=f)

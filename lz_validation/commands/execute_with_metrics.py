#!/usr/bin/env python
'''
for testing install 'stress' package and run

\b
    export OUTPUT_DIR=<existing folder>
    lz_validation execute_with_metrics stress --cpu 1 --io 1 --vm 1 --vm-bytes 128M --timeout 10s --verbose
'''
from __future__ import print_function
import subprocess
import sys
import os
import resource
import json
import logging
import errno
import click


def monitor_command(command):
    usage_start = resource.getrusage(resource.RUSAGE_CHILDREN)
    for line in execute(command):
        print(line, end="")
    usage_end = resource.getrusage(resource.RUSAGE_CHILDREN)

    max_rss_in_MB = (usage_end.ru_maxrss - usage_start.ru_maxrss) / 1024.
    metrics = dict(
        cpu_time_in_s=usage_end.ru_utime - usage_start.ru_utime,
        max_rss_in_MB=round(max_rss_in_MB, 1),
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


def save_to_file(metrics, metrics_file):
    if os.path.exists(metrics_file):
        with open(metrics_file) as f:
            metrics.update(json.load(f))
    with open(metrics_file, 'w') as f:
        json.dump(metrics, f)


def print_metrics(metrics):
    command = metrics.keys()[0]
    params = dict(command=command)
    params.update(metrics[command])
    msg = [
        '>>> Ran command: "{command}"',
        '>>> in {cpu_time_in_s}s and used {max_rss_in_MB} MB of memory.'
    ]
    msg = '\n'.join(msg)
    print(msg.format(**params))


@click.command(help=__doc__)
@click.argument('command')
@click.option('--metrics-file', default='metrics.json')
def cli(command, output_folder, metrics_file):
    metrics = monitor_command(command.split())
    print_metrics(metrics)
    save_to_file(metrics, metrics_file)

if __name__ == '__main__':
    command = sys.argv[1:]
    metrics = monitor_command(command)

    print_metrics(metrics)

    job_name = os.environ.get('CI_JOB_NAME', 'no_job_name')
    output_folder = os.environ.get('OUTPUT_DIR', '/tmp')
    metrics_file = '{output_folder}/metrics_{job_name}.json'
    metrics_file = metrics_file.format(
        output_folder=output_folder, job_name=job_name)
    save_to_file(metrics, metrics_file)

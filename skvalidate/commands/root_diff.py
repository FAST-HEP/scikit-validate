"""Calculates the difference between two ROOT (https://root.cern.ch/) files.

If a difference is present, the command will create plots for the distributions that differ.

TODO: separate functionality: plotting, recursive reading of ROOT files, diff calculation
TODO: allow for injection of user-defined high-level variables
"""
from __future__ import print_function
import os
import threading

import click
import numpy as np
from plumbum import colors
from tqdm import tqdm

from skvalidate import compare
from skvalidate.vis import draw_diff
from skvalidate.io import write_data_to_json


class ProcessStatus(threading.Thread):

    def __init__(self, name, values, output_path):
        threading.Thread.__init__(self)
        self.name = name
        self.values = values
        self.output_path = output_path
        self.color = colors.red
        self.msg = compare.ERROR

    def run(self):
        evaluationValue = self.values['evaluationValue']
        status = self.values['status']
        if status == compare.FAILED:
            image = draw_diff(self.name, self.values, self.output_path)
            self.values['image'] = image
            self.msg = 'FAILED (test: {:0.3f}): {}'.format(evaluationValue, image)
        if status == compare.UNKNOWN:
            self.msg = 'WARNING: Unable to compare (value type: {})'.format(self.values['original'].dtype)
            self.color = colors.Orange3
        if status == compare.SUCCESS:
            self.msg = 'OK'
            self.color = colors.green
        self.values['msg'] = self.msg
        del self.values['original']
        del self.values['reference']
        del self.values['diff']


@click.command()
@click.argument('file_under_test', type=click.Path(exists=True))
@click.argument('reference_file', type=click.Path(exists=True))
@click.option('-o', '--output-path', type=click.Path(exists=True), required=True)
@click.option('-r', '--report-file', type=click.Path(), default='root_comparison.json')
@click.option('-p', '--prefix', default=os.environ.get('CI_JOB_NAME', 'root_diff'))
def cli(file_under_test, reference_file, output_path, report_file, prefix):
    # TODO add verbosity setting
    # TODO: add parameter for distributions that are allowed to file (e.g. timestamps)
    # TODO: throw error if any distribution fails
    comparison = compare.compare_two_root_files(file_under_test, reference_file)
    comparison = _reset_infinities(comparison)

    print('Testing {0} distributions'.format(len(comparison)))
    threads = {}
    for name in sorted(comparison.keys()):
        values = comparison[name]
        thread = ProcessStatus(name, values, output_path)
        thread.start()
        threads[name] = thread

    for name, thread in tqdm(threads.items()):
        thread.join()
        print(thread.color | '{0} - {1}'.format(thread.name, thread.msg))
        comparison[name] = thread.values

    summary = _add_summary(comparison, prefix)
    summary[prefix]['output_path'] = output_path
    # TODO: print nice summary
    write_data_to_json(summary, report_file)


def _reset_infinities(comparison):
    for name, values in comparison.items():
        if values['original'].dtype.kind in {'U', 'S', 'O'}:
            continue
        if len(values['original']) > 0:
            values['original'][np.absolute(values['original']) == np.Infinity] = 0
        if len(values['reference']) > 0:
            values['reference'][np.absolute(values['reference']) == np.Infinity] = 0
        if len(values['diff']) > 0:
            values['diff'][np.absolute(values['diff']) == np.Infinity] = 0
        comparison[name] = values
    return comparison


def _add_summary(comparison, prefix):
    summary = {}
    summary['distributions'] = comparison
    summary[compare.FAILED] = []
    summary[compare.UNKNOWN] = []
    summary[compare.SUCCESS] = []
    summary[compare.ERROR] = []
    for name, values in comparison.items():
        status = values['status']
        summary[status].append(name)

    return {prefix: summary}

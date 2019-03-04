"""Calculates the difference between two ROOT (https://root.cern.ch/) files.

If a difference is present, the command will create plots for the distributions that differ.

TODO: separate functionality: plotting, recursive reading of ROOT files, diff calculation
TODO: allow for injection of user-defined high-level variables
"""
from __future__ import print_function
import os

import click
import numpy as np
from plumbum import colors

from skvalidate import compare
from skvalidate.vis import draw_diff
from skvalidate.io import write_data_to_json


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
    for name in sorted(comparison.keys()):
        values = comparison[name]
        status = values['status']
        msg = compare.ERROR
        color = colors.red
        if status == compare.FAILED:
            image = draw_diff(name, values, output_path)
            values['image'] = image
            msg = 'FAILED: ' + image
        if status == compare.UNKNOWN:
            msg = 'WARNING: Unable to compare'
            color = colors.orange
        if status == compare.SUCCESS:
            msg = 'OK'
            color = colors.green

        values['msg'] = msg
        # TODO: only print this for verbose option
        print(color | '{0} - {1}'.format(name, msg))
        # drop arrays from comparison
        del values['original']
        del values['reference']
        del values['diff']
        comparison[name] = values

    summary = _add_summary(comparison, prefix)
    summary[prefix]['output_path'] = output_path
    # TODO: print nice summary
    write_data_to_json(summary, report_file)


def _reset_infinities(comparison):
    for name, values in comparison.items():
        values['original'][np.absolute(values['original']) == np.Infinity] = 0
        values['reference'][np.absolute(values['reference']) == np.Infinity] = 0
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

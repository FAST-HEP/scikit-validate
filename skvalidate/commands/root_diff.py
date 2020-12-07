"""Calculates the difference between two ROOT (https://root.cern.ch/) files.

If a difference is present, the command will create plots for the distributions that differ.

TODO: separate functionality: plotting, recursive reading of ROOT files, diff calculation
TODO: allow for injection of user-defined high-level variables
"""
from __future__ import print_function
import multiprocessing as mp
import os
import threading

import awkward as ak
import click
from plumbum import colors
from tqdm import tqdm

from skvalidate import compare
from skvalidate.vis import draw_diff
from skvalidate.io import write_data_to_json


def _process(name, values, output_path):
    color = colors.red
    msg = compare.ERROR

    status = values['status']

    if status == compare.FAILED:
        try:
            image = draw_diff(name, values, output_path)
            values['image'] = image
            msg = 'FAILED (reason: {}): {}'.format(values['reason'], image)
        except TypeError as e:
            msg = 'ERROR: Cannot draw (value types: {0} & {1}, reason: {2})'.format(
                "NoneType" if values['original'] is None else str(ak.type(values['original'])),
                "NoneType" if values['reference'] is None else str(ak.type(values['reference'])),
                str(e),
            )
    if status == compare.UNKNOWN:
        msg = 'WARNING: Unable to compare (value type: {0}, reason: {1})'.format(
            "Unknown" if values['original'] is None else str(ak.type(values['original'])),
            values['reason'],
        )
        color = colors.Orange3
    if status == compare.SUCCESS:
        msg = 'OK'
        color = colors.green
    values['msg'] = msg
    values['color'] = color

    del values['original']
    del values['reference']
    del values['diff']

    return values


class MultiProcessStatus(object):

    def __init__(self, comparison, n_processes, output_path):
        self.comparison = comparison
        self.pool = mp.Pool(n_processes)
        self.n_cores = n_processes
        self.output_path = output_path
        self.n_comparisons = len(comparison)
        self.pbar = tqdm(self.n_comparisons)

    def runMultiProcessing(self):
        print('Testing {0} distributions'.format(self.n_comparisons))
        results = {}
        for name in sorted(self.comparison.keys()):
            result = self.pool.apply_async(
                _process,
                args=(name, self.comparison[name], self.output_path),
                callback=self._update,
            )
            results[name] = result
        self.pool.close()
        self.pool.join()
        for name in results.keys():
            self.comparison[name] = results[name].get()

    def runSingleCore(self):
        print('Testing {0} distributions'.format(self.n_comparisons))
        for name in sorted(self.comparison.keys()):
            result = _process(name, self.comparison[name], self.output_path)
            self.comparison[name] = result

    def run(self):
        if self.n_cores > 1:
            self.runMultiProcessing()
        else:
            self.runSingleCore()

    def runMultiThread(self):
        print('Testing {0} distributions'.format(self.n_comparisons))
        threads = {}
        for name in sorted(self.comparison.keys()):
            thread = threading.Thread(target=_process, args=(name, self.comparison[name], self.output_path))
            thread.daemon = True
            thread.start()
            threads[name] = thread

        for name, thread in threads.items():
            thread.join()
            self._update()
            self.comparison[name] = thread.values

    def _update(self, *a):
        self.pbar.update()

    def terminate(self):
        self.pool.terminate()
        self.pool.join()


@click.command()
@click.argument('file_under_test', type=click.Path(exists=True))
@click.argument('reference_file', type=click.Path(exists=True))
@click.option('-o', '--output-path', type=click.Path(exists=True), required=True)
@click.option('-r', '--report-file', type=click.Path(), default='root_comparison.json')
@click.option('-p', '--prefix', default=os.environ.get('CI_JOB_NAME', 'root_diff'))
@click.option('-n', '--n-cores', default=1, type=int, help='Experimental feature: use n number of cores')
def cli(file_under_test, reference_file, output_path, report_file, prefix, n_cores):
    # TODO add verbosity setting
    # TODO: add parameter for distributions that are allowed to fail (e.g. timestamps)
    # TODO: throw error if any distribution fails
    summary = {}
    for name, comparison in compare.compare_two_root_files(file_under_test, reference_file):
        comparison = _reset_infinities(comparison)
        if comparison is None:
            continue
        result = _process(name, comparison, output_path)
        print(result['color'] | f'{name} - {result["msg"]}')
        del result['color']  # delete, as we cannot JSON it
        summary[name] = result

    # processing = MultiProcessStatus(comparison, n_cores, output_path)
    # try:
    #     processing.run()
    # except KeyboardInterrupt:
    #     processing.terminate()

    # summary = _add_summary(processing.comparison, prefix)
    summary = _add_summary(summary, prefix)
    summary[prefix]['output_path'] = output_path
    # TODO: print nice summary
    write_data_to_json(summary, report_file)


def _reset_infinities(comparison):
    if comparison['original'] is None or comparison['reference'] is None:
        return None
    if 'str' in str(ak.type(comparison['original'])):
        return None
    if 'str' in str(ak.type(comparison['reference'])):
        return None
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

"""
    Display the difference between two metric (JSON) files.

    Examples:
        sv_metric_diff skvalidate/data/examples/performance_metrics*.json
        sv_metric_diff skvalidate/data/examples/file_metrics*.json
"""
import json
import os

import click
from jinja2 import Template
import pandas as pd
from tabulate import tabulate

from skvalidate.compare import compare_metrics
from skvalidate import __skvalidate_root__

def print_console(results, **kwargs):
    to_print = results[results.metric != 'size_in_bytes']
    print(tabulate(to_print, headers='keys', tablefmt='psql', showindex=False))


def print_csv(results, **kwargs):
    print(results.to_csv(index=False))


def print_markdown(results, **kwargs):
    title = kwargs.pop('title')
    template_file = 'file_metrics.md' if title == 'file' else 'performance.md'
    path = [__skvalidate_root__, 'data', 'templates', 'report', 'default', template_file]
    template_file = os.path.join(*path)
    with open(template_file) as f:
        template = Template(f.read())
    print(template.render(comparison=results))


OUTPUT = dict(
    console=print_console,
    csv=print_csv,
    markdown=print_markdown,
)


def expand_results(results, title_desc):
    """Creates one row per result & metric combination"""
    expanded_results = []
    headers = [title_desc, 'metric', 'value', 'ref value', 'diff', 'diff_pc', 'unit']
    for title, measurement in results.items():
        for name, metric in measurement.items():
            result = [title, name, metric['value'], metric['ref'], metric['diff'], metric['diff_pc'], metric['unit']]
            expanded_results.append(result)
    return pd.DataFrame(expanded_results, columns=headers)


@click.command(help=__doc__)
@click.argument('file_under_test', type=click.Path(exists=True))
@click.argument('reference_file', type=click.Path(exists=True))
@click.option('-o', '--output-format', type=click.Choice(['console', 'csv', 'markdown']), default='console')
def cli(file_under_test, reference_file, output_format):
    results = {}
    with open(file_under_test) as f:
        test_data = json.load(f)
    with open(reference_file) as f:
        ref_data = json.load(f)

    results = compare_metrics(test_data, ref_data)

    metric_types = []
    for title, measurement in test_data.items():
        for name, metric in measurement.items():
            if 'time' in name:
                metric_types.append('time')
            if 'rss' in name:
                metric_types.append('rss')
            if 'size' in name:
                metric_types.append('size')

    title = 'unknown'
    if 'time' in metric_types and 'rss' in metric_types:
        title = 'command'
    if 'size' in metric_types and 'rss' not in metric_types:
        title = 'file'

    if not output_format == 'markdown':
        results = expand_results(results, title_desc=title)
    OUTPUT[output_format](results, title=title)

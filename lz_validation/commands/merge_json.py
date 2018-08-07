'''
Merges <N>JSON files into one output file
'''
import click
import json


@click.command(help=__doc__)
@click.argument('input_files', type=click.Path(exists=True), nargs=-1)
@click.argument('output', nargs=1)
def cli(input_files, output):
    summary = {}
    for i in input_files:
        with open(i) as f:
            summary.update(json.load(f))

    with open(output, 'w') as f:
        json.dump(summary, f)

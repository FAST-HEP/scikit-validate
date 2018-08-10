"""
Command for inspecting the size of branches in a ROOT file
"""
from __future__ import print_function

import logging
import warnings
# pandas might show some warnings
warnings.filterwarnings('ignore')

import click
import pandas
import uproot

from lz_validation.io import root_walk

logging.basicConfig(level=logging.INFO)


@click.command()
@click.argument('input-file', type=click.Path(exists=True))
@click.option('--output-file')
def cli(input_file, output_file):
    f = uproot.open(input_file)
    e = f['MCTruthTree']['MCTruthEvent']
    b = f['MCTruthTree']['MCTruthEvent']['fReferencePhotonTime_ns']

    results = [inspect_size(name, obj) for (name, obj) in root_walk(f)]
    df = pandas.DataFrame.from_dict(results)
    order = ['name', 'interpretation', 'uncompressedbytes', 'compressedbytes', 'compressionratio', 'fZipBytes','fTotBytes']
    df = df[order]
    print(df)


def inspect_size(name, branch):
    """
    Return sizes (compressed/uncompressed) and inferred type
    """
    attrs = ['fTotBytes', 'interpretation', 'compressedbytes', 'fZipBytes', ]
    methods = ['compressedbytes', 'uncompressedbytes', 'compressionratio']
    result = dict(name=name)
    # result['uncompressedbytes'] = getattr(branch, 'uncompressedbytes')()
    for attr in attrs:
        result[attr] = getattr(branch, attr)
    for method in methods:
        result[method] = getattr(branch, method)()
    return result

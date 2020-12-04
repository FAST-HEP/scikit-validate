"""
Read a ROOT file and reports information about its content (names, sizes, types)
"""
from __future__ import print_function
import click
import numpy as np
import pandas as pd
from tabulate import tabulate
import uproot

from skvalidate.io import _walk


def info(input_file):
    f = uproot.open(input_file)

    data = []
    labels = ['name', 'type', 'interpretation', 'compressedbytes',
              'uncompressedbytes', 'hasStreamer', 'uproot_readable', 'is_empty']
    for name, obj in _walk(f):
        canRead = False
        is_empty = False
        typename = obj.typename
        hasStreamer = hasattr(obj, '_streamer') and obj._streamer is not None
        interpretation = obj.interpretation if hasattr(obj, 'interpretation') else None
        if not hasStreamer and interpretation is None:
            data.append(
                (name, typename, interpretation, np.nan, np.nan, hasStreamer, canRead, is_empty)
            )
            continue

        try:
            a = obj.array()
            if a is None or len(a) == 0:
                is_empty = True
            # try to access first element
            if not is_empty:
                a[0]
            canRead = True
        except Exception as e:
            print(e)
        data.append(
            (name, typename, interpretation, obj.compressed_bytes,
             obj.uncompressed_bytes, hasStreamer, canRead, is_empty)
        )
    return pd.DataFrame.from_records(data, columns=labels)


@click.command(help=__doc__)
@click.argument('input_file', type=click.Path(exists=True))
@click.option('-o', '--output-file', help="CSV output file for information", type=click.Path(), default='root_info.csv')
@click.option('--show-unreadable', help="print the file entries that uproot cannot read", default=False, is_flag=True)
@click.option('--show-empty', help="print the file entries that are empty", default=False, is_flag=True)
@click.option('-q', '--quiet', help="print only failures", default=False, is_flag=True)
def cli(input_file, output_file, show_unreadable, show_empty, quiet):
    df = info(input_file)
    if not quiet and not (show_unreadable or show_empty):
        print(tabulate(df, headers='keys', tablefmt='psql'))
    if show_unreadable:
        unreadable = df[~df.uproot_readable]
        if unreadable.empty:
            print('All file contents can be read by uproot')
        else:
            print('The following file contents cannot be read by uproot')
            print(tabulate(unreadable, headers='keys', tablefmt='psql'))
    print()
    if show_empty:
        empty = df[df.is_empty]
        if empty.empty:
            print('All file contents are filled')
        else:
            print('The following file contents are empty')
            print(tabulate(empty, headers='keys', tablefmt='psql'))
    df.to_csv(output_file)

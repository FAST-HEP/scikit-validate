"""
Read a ROOT file and reports information about its content (names, sizes, types)
"""
import click
import pandas as pd
from tabulate import tabulate
import uproot

from skvalidate.io import _walk


def info(input_file):
    f = uproot.open(input_file)

    data = []
    labels = ['name', 'uproot_type', 'compressedbytes', 'uncompressedbytes', 'hasStreamer', 'uproot_readable']
    for name, obj in _walk(f):
        canRead = False
        try:
            obj.array()
            canRead = True
        except Exception:
            pass
        hasStreamer = obj._streamer is not None
        data.append((name, obj.interpretation, obj.compressedbytes(), obj.uncompressedbytes(), hasStreamer, canRead))
    return pd.DataFrame.from_records(data, columns=labels)


@click.command(help=__doc__)
@click.argument('input_file', type=click.Path(exists=True))
@click.option('-o', '--output-file', help="CSV output file for information", type=click.Path(), default='root_info.csv')
@click.option('--show-unreadable', help="print the file entries that uproot cannot read", default=False, is_flag=True)
@click.option('-v', '--verbose', help="print information", default=False, is_flag=True)
def cli(input_file, output_file, show_unreadable, verbose):
    df = info(input_file)
    if verbose and not show_unreadable:
        print(tabulate(df, headers='keys', tablefmt='psql'))
    if show_unreadable:
        unreadable = df[df.uproot_readable == False]
        if unreadable.empty:
            print('All file contents can be read by uproot')
        else:
            print('The following file contents cannot be read by uproot')
            print(tabulate(unreadable, headers='keys', tablefmt='psql'))
    df.to_csv(output_file)

"""
Calculates the difference between two ROOT (https://root.cern.ch/) files.
If a difference is present, the command will create plots for the distributions that differ.

TODO: separate functionality: plotting, recursive reading of ROOT files, diff calculation
TODO: allow for injection of user-defined high-level variables

"""
from __future__ import print_function
import click

from skvalidate.io import walk
from skvalidate import compare
from skvalidate.vis import draw_diff


@click.command()
@click.argument('file_under_test', type=click.Path(exists=True))
@click.argument('reference_file', type=click.Path(exists=True))
@click.option('--out-dir', type=click.Path(exists=True))
def cli(file_under_test, reference_file, out_dir):
    assert out_dir is not None
    are_OK, are_not_OK = _compare(file_under_test, reference_file)

    outfiles = []
    for o_name, values in are_not_OK:
        outfiles.append(draw_diff(o_name, values, out_dir))

    print('Testing distributions')
    for name, _ in are_OK:
        print(name, '- OK')

    if any(are_not_OK):
        print('WARNING: following distributions differ')
        for f, (name, (_, _, diff)) in zip(outfiles, are_not_OK):
            print('{0}: {1}'.format(name, f), diff)

    # TODO: produce validatition report dict


def _compare(path, ref_path):
    are_OK = []
    are_not_OK = []

    for (o_name, orig), (ref_name, ref) in zip(walk(path), walk(ref_path)):
        if o_name != ref_name:
            continue
            raise ValueError(
                'Comparing two different entries {0} vs {1}'.format(o_name, ref_name))
        diff = compare.difference(ref, orig)
        if not compare.is_ok(diff, tolerance=0.02):
            are_not_OK.append((o_name, (orig, ref, diff)))
        else:
            are_OK.append((o_name, (orig, ref, diff)))
    return are_OK, are_not_OK

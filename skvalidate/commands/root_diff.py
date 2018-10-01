"""
Calculates the difference between two ROOT (https://root.cern.ch/) files.
If a difference is present, the command will create plots for the distributions that differ.

TODO: separate functionality: plotting, recursive reading of ROOT files, diff calculation
TODO: allow for injection of user-defined high-level variables

"""
from __future__ import print_function
import os
import uproot
import numpy as np
import click

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


@click.command()
@click.argument('file_under_test', type=click.Path(exists=True))
@click.argument('reference_file', type=click.Path(exists=True))
@click.option('--out-dir', type=click.Path(exists=True))
def cli(file_under_test, reference_file, out_dir):
    assert out_dir is not None
    are_OK, are_not_OK = _compare_mctruth(file_under_test, reference_file)

    outfiles = []
    for o_name, values in are_not_OK:
        outfiles.append(draw_diff(o_name, values, out_dir))

    print('Testing distributions')
    for name in are_OK:
        print(name, '- OK')

    if any(are_not_OK):
        print('WARNING: following distributions differ')
        for f in outfiles:
            print(f)

    # TODO: produce validatition report dict


def _walk(obj):
    for k in sorted(obj.allkeys()):
        try:
            yield k.decode("utf-8"), obj[k].array()
        except Exception:
            for n, o in _walk(obj[k]):
                yield '{0}.{1}'.format(k.decode("utf-8"), n), o


def _compare_mctruth(path, ref_path):
    mctruth = uproot.open(path)
    ref_mctruth = uproot.open(ref_path)
    are_OK = []
    are_not_OK = []

    for (o_name, orig), (ref_name, ref) in zip(_walk(mctruth), _walk(ref_mctruth)):
        if o_name != ref_name:
            continue
            raise ValueError(
                'Comparing two different entries {0} vs {1}'.format(o_name, ref_name))
        diff = _diff(ref, orig)
        if not _isOK(diff, ref, orig):
            are_not_OK.append((o_name, (orig, ref, diff)))
        else:
            are_OK.append(o_name)
    return are_OK, are_not_OK


def _diff(n1, n2):
    try:
        return n1 - n2
    except Exception:
        return [0]  # TODO: need to compare string as well?


def _isOK(diff, ref, orig):
    if len(diff) == 0:
        return len(ref) == len(orig)
    isOKMaxDiff = 0.02  # 2%
    d = np.absolute(diff)
    norm = np.linalg.norm(d)
    if norm == 0:
        return True
    d = d / norm
    return max(d) < isOKMaxDiff


def store_diff(name, diff, out_dir):
    out = os.path.join(out_dir, name + '.npy')
    np.save(out, diff)


def draw_diff(name, values, out_dir):
    orig, ref, diff = values
    orig_hist, bins = np.histogram(orig, 100)
    ref_hist, _ = np.histogram(ref, bins)
    diff = orig_hist - ref_hist

    fig, (a0, a1) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [5, 1]}, sharex=True)
    name = name.replace(';1', '')
    output_file = os.path.join(out_dir, name + '.png')

    a0.hist(orig_hist, label='this code', color='red', histtype='step', bins=bins, linewidth=2, alpha=0.6)
    a0.hist(ref_hist, label='reference', color='black', histtype='step', bins=bins)
    a0.set_ylabel('a.u.')
    a0.set_yscale('log', nonposy='clip')
    a0.legend()
    a0.set_title('Validation plot: Work in Progress - handle with grain of salt')

    a1.hist(diff, label='diff', histtype='step', bins=bins)
    a1.set_xlabel(name)
    a1.minorticks_on()
    a1.legend()

    fig.tight_layout()
    plt.savefig(output_file)
    plt.close()
    return output_file

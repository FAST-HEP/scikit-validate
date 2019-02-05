import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from scipy import stats


def adjust_axis_limits(a_min, a_max, change=0.2, logy=False):
    a_min = a_min * (1 + change) if a_min < 0 else a_min * (1 - change)
    a_max = a_max * (1 + change) if a_max > 0 else a_max * (1 - change)
    if logy and a_min <= 0:
        a_min = 1e-1
    return a_min, a_max


def find_limits(d_1, d2):
    a_min = min(min(d_1), min(d2))
    a_max = max(max(d_1), max(d2))
    return a_min, a_max


def draw_diff(name, values, out_dir, bins=100):
    logy = False

    orig, ref, diff = values
    bins = 100

    min_x, max_x = find_limits(orig, ref)
    min_x, max_x = adjust_axis_limits(min_x, max_x, change=0.1)

    fig, (a0, a1) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [5, 1]}, sharex=True)
    name = name.replace(';1', '')
    output_file = os.path.join(out_dir, name + '.png')

    h_ref, bin_edges, _ = a0.hist(
        ref, label='reference', color='black', histtype='step', bins=bins, range=(min_x, max_x),
    )
    h_orig, _, _ = a0.hist(
        orig, label='this code', color='red', histtype='step', bins=bin_edges, linewidth=2, alpha=0.6,
        range=(min_x, max_x),
    )

    min_y, max_y = find_limits(h_ref, h_orig)
    if max_y - min_y > 1e3:
        logy = True
    if max_y <= 0 and min_y <= 0:
        logy = False
    min_y, max_y = adjust_axis_limits(min_y, max_y, logy=logy)
    a0.set_ylim(min_y, max_y)
    a0.legend()

    ks_statistic, pvalue = stats.ks_2samp(ref, orig)
    a0.set_title('{0} \n KS statistic: {1:.3f}; p-value: {2:.3f}'.format(name, ks_statistic, pvalue))

    a1.plot(bin_edges[1:], h_ref - h_orig, label='difference', drawstyle='steps',)
    a1.set_xlabel(name)
    # a1.minorticks_on()
    min_y, max_y = a1.get_ylim()
    min_y, max_y = adjust_axis_limits(min_y, max_y)
    a1.set_ylim(min_y, max_y)
    a1.locator_params(axis='y', nbins=4)
    a1.legend()

    if logy:
        a0.set_yscale('log', nonposy='clip')
        # a1.set_yscale('log', nonposy='clip')

    fig.tight_layout()
    plt.savefig(output_file)
    plt.close()
    return output_file

"""
Visualization package
"""
import os

import numpy as np
import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['lines.linewidth'] = 4
matplotlib.rcParams['axes.titlesize'] = 40
matplotlib.rcParams['axes.labelsize'] = 32
matplotlib.rcParams['figure.titlesize'] = 40
matplotlib.rcParams['legend.fontsize'] = 32
matplotlib.rcParams['patch.linewidth'] = 4
matplotlib.rcParams['xtick.labelsize'] = 32
matplotlib.rcParams['ytick.labelsize'] = 32

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

from .profile import draw_profiles


def adjust_axis_limits(a_min, a_max, change=0.2, logy=False):
    a_min = a_min * (1 + change) if a_min < 0 else a_min * (1 - change)
    a_max = a_max * (1 + change) if a_max > 0 else a_max * (1 - change)
    if logy and a_min <= 0:
        a_min = 1e-1
    return a_min, a_max


def find_limits(d1, d2):
    if (d1 is None and d2 is None) or (np.size(d1) == 0 and np.size(d2) == 0):
        return 0, 0
    if d1 is None or np.size(d1) == 0:
        return np.amin(d2), np.amax(d2)
    if d2 is None or np.size(d2) == 0:
        return np.amin(d1), np.amax(d1)

    a_min = min(np.amin(d1), np.amin(d2))
    a_max = max(np.amax(d1), np.amax(d2))
    return a_min, a_max


def draw_diff(name, values, output_path, bins=100):
    name = name.replace(';1', '')
    output_file = os.path.join(output_path, name + '.png')
    logy = False

    min_x, max_x = find_limits(values['original'], values['reference'])
    min_x, max_x = adjust_axis_limits(min_x, max_x, change=0.1)

    fig = Figure(figsize=(20, 20))
    canvas = FigureCanvas(fig)  # noqa: F841
    a0, a1 = fig.subplots(2, 1, gridspec_kw={'height_ratios': [5, 1]}, sharex=True, )

    if values['reference'] is not None and np.size(values['reference']) != 0:
        h_ref, bin_edges, _ = a0.hist(
            values['reference'], label='reference', color='black', histtype='step', bins=bins, range=(min_x, max_x),
        )
    else:
        h_ref, bin_edges, _ = a0.hist(
            [-1], label='reference (missing)', color='black', histtype='step', bins=bins, range=(min_x, max_x),
        )
    if values['original'] is not None and np.size(values['original']) != 0:
        h_orig, _, _ = a0.hist(
            values['original'], label='this code', color='red', histtype='step', bins=bin_edges, linewidth=2, alpha=0.6,
            range=(min_x, max_x),
        )
    else:
        h_orig, _, _ = a0.hist(
            [-1], label='this code (missing)', color='red', histtype='step', bins=bin_edges, linewidth=2, alpha=0.6,
            range=(min_x, max_x),
        )

    min_y, max_y = find_limits(h_ref, h_orig)
    if max_y - min_y > 1e3:
        logy = True
    if max_y <= 0 and min_y <= 0:
        logy = False
    min_y, max_y = adjust_axis_limits(min_y, max_y, logy=logy)
    a0.set_ylim(min_y, max_y)
    a0.legend(loc='upper center', bbox_to_anchor=(0.5, 1.00), ncol=2)

    ks_statistic, pvalue = values['ks_statistic'], values['pvalue']
    a0.set_title('{0} \n KS statistic: {1:.3f}; p-value: {2:.3f}'.format(name, ks_statistic, pvalue))

    a1.plot(bin_edges[1:], h_ref - h_orig, label='difference', drawstyle='steps',)
    a1.set_xlabel(name)
    # a1.minorticks_on()
    min_y, max_y = a1.get_ylim()
    min_y, max_y = adjust_axis_limits(min_y, max_y)
    a1.set_ylim(min_y, max_y)
    a1.locator_params(axis='y', nbins=4)
    a1.legend(loc='upper center', bbox_to_anchor=(0.5, 1.00))

    if logy:
        a0.set_yscale('log', nonposy='clip')
        # a1.set_yscale('log', nonposy='clip')

    fig.tight_layout()
    fig.savefig(output_file)
    return output_file


__all__ = [
    'draw_diff',
    'draw_profiles',
]

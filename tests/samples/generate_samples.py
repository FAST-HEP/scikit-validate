"""
Run from main directory.

Usage:
    python tests/samples/generate_samples.py
"""
import numpy as np
from random import gauss, sample
from string import ascii_letters
import types

import six
import uproot
import uproot_methods.classes.TGraph

class MyGraph(uproot_methods.classes.TGraph.Methods, list):
    def __init__(self, low, high, values, title=""):
        self._fXaxis = types.SimpleNamespace()
        self._fXaxis._fNbins = len(values)
        self._fXaxis._fXmin = low
        self._fXaxis._fXmax = high
        for x in values:
            self.append(float(x))
        self._fTitle = title
        self._classname = "TGraph"


def generate_root_data(output_file='tests/samples/test_1.root', branches={'x': 'F', 'y': 'F', 'z': 'F', 'i': 'I'}):
    """From http://www.rootpy.org/modules/trees.html."""
    from rootpy.tree import Tree
    from rootpy.io import root_open
    f = root_open(output_file, 'recreate')
    tree = Tree('test')
    tree.create_branches(branches)

    for i in six.moves.xrange(10000):
        tree.x = gauss(.5, 1.)
        tree.y = gauss(.3, 2.)
        tree.z = gauss(13., 42.)
        tree.i = i
        if 'a' in branches:
            tree.a = gauss(.1, 1.)
        if 'string' in branches:
            tree.string = (u''.join(sample(ascii_letters, 4))).encode('ascii')
        for v in six.moves.xrange(10):
            tree.v[v] = gauss(.5, 1.)
        tree.fill()
    tree.write()

    f.close()


def generate_graphs_and_histograms(output_file='tests/samples/non_tree_objects.root'):
    with uproot.recreate(output_file, compression=uproot.ZLIB(4)) as f:
        f['1Dhist'] = np.histogram(np.random.normal(0, 1, 10000))
        f['2Dhist'] = np.histogram2d(np.random.normal(0, 1, 10000), np.random.normal(0, 1, 10000))
        # not yet supported
        # f['TGraph'] = MyGraph(0, 1, np.random.normal(0, 1, 10000), "TGraph")


if __name__ == '__main__':
    branches = {'x': 'F', 'y': 'F', 'z': 'F', 'i': 'I', 'v': 'F[10]', 'string': 'C[5]'}
    generate_root_data('tests/samples/test_1.root', branches)
    generate_root_data('tests/samples/test_2.root', branches)
    branches = {'x': 'F', 'y': 'F', 'z': 'F', 'i': 'I', 'v': 'F[10]', 'a': 'F'}
    generate_root_data('tests/samples/test_3.root', branches)

    generate_graphs_and_histograms('tests/samples/non_tree_objects.root')

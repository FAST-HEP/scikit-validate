"""
Run from main directory.

Usage:
    python tests/samples/generate_samples.py
"""
from random import gauss

import six


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
        for v in six.moves.xrange(10):
            tree.v[v] = gauss(.5, 1.)
        tree.fill()
    tree.write()

    f.close()


if __name__ == '__main__':
    branches = {'x': 'F', 'y': 'F', 'z': 'F', 'i': 'I', 'v': 'F[10]'}
    generate_root_data('tests/samples/test_1.root', branches)
    generate_root_data('tests/samples/test_2.root', branches)
    branches = {'x': 'F', 'y': 'F', 'z': 'F', 'i': 'I', 'v': 'F[10]', 'a': 'F'}
    generate_root_data('tests/samples/test_3.root', branches)

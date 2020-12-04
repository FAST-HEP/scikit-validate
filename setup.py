#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

import codecs
import os
import glob
import re
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    global here
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


def _is_valid_command(file_name):
    with open(file_name) as f:
        return 'def cli(' in f.read()


def find_commands(path=os.path.join('skvalidate','commands')):
    """ Scans path for valid commands """
    command_files = glob.glob(os.path.join(path, '*.py'))
    # commands = []
    for file_name in command_files:
        if not _is_valid_command(file_name):
            continue
        command_path = file_name.replace('.py', '').replace(os.path.sep, '.')
        name = command_path.split('.')[-1]
        yield'sv_{name}={path}:cli'.format(name=name, path=command_path)

        # execute_with_metrics=skvalidate.commands.execute_with_metrics:cli


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'awkward>=1.0.0rc2',
    'Click<8.0',
    'gitpython<4.0.0',
    'fuzzywuzzy',
    'jinja2',
    'markdown2',
    'matplotlib<4.0.0',
    'memory_profiler>=0.54',
    'numexpr',
    'numpy>=1.19.0',
    'pandas',
    'plumbum',
    'python-gitlab<3.0.0',
    'python-Levenshtein',
    'pyyaml',
    'scipy',
    'tabulate',
    'tqdm',
    'uproot>=4.0.0rc2',
    'xhtml2pdf',
]

setup_requirements = [
    # 'pytest-runner',
]

test_requirements = [
    'coverage',
    'httmock',
    'hypothesis',
    'mock',
    'pytest',
    'pytest-cov',
    'responses',
]

setup(
    author="Luke Kreczko",
    author_email='kreczko@cern.ch',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    description="Science validation toolkit",
    entry_points={
        'console_scripts': [
            # 'skvalidate=skvalidate.cli:main',
            'run-clang-tidy=skvalidate.clang_tidy:main',
        ] + list(find_commands()),
    },
    install_requires=requirements,
    license="Apache Software License 2.0",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='skvalidate',
    name='scikit-validate',
    packages=find_packages(include=[
        'skvalidate',
        'skvalidate.commands',
        'skvalidate.compare',
        'skvalidate.gitlab',
        'skvalidate.io',
        'skvalidate.operations',
        'skvalidate.report',
        'skvalidate.software',
        'skvalidate.vis',
    ]),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://gitlab.cern.ch/fast-hep/public/scikit-validate',
    version=find_version("skvalidate", '__init__.py'),
    zip_safe=False,
)

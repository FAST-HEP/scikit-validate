#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=6.0', 'python-gitlab']

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="Luke Kreczko",
    author_email='kreczko@cern.ch',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    description="LZ physics validation package",
    entry_points={
        'console_scripts': [
            'lz_validation=lz_validation.cli:main',
            'run-clang-tidy=lz_validation.clang_tidy:main',
        ],
    },
    install_requires=requirements,
    license="Apache Software License 2.0",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='lz_validation',
    name='lz_validation',
    packages=find_packages(include=['lz_validation']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/kreczko/lz_validation',
    version='0.0.1',
    zip_safe=False,
)

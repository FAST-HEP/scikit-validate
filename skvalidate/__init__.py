# -*- coding: utf-8 -*-

"""Top-level package for scikit-validate."""
import logging
import os

__author__ = """FAST"""
__email__ = 'fast-hep@cern.ch'
__version__ = '0.2.13'

__skvalidate_root__ = os.path.dirname(__file__)


# logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# add loggers
ch = logging.StreamHandler()
if not os.environ.get("SK_DEBUG", False):
    ch.setLevel(logging.INFO)
else:
    ch.setLevel(logging.DEBUG)

# log format
formatter = logging.Formatter(
    '%(asctime)s [%(name)s]  %(levelname)s: %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `skvalidate` package."""

from click.testing import CliRunner

from skvalidate.commands.remove_from_env import cli


def test_path_includes_item():
    path = ':'.join(['/a/b/c', '/a/b/d', '/d/c/s'])
    remove = '/a/b'

    runner = CliRunner()
    result = runner.invoke(cli, [path, remove])
    assert result.output == '/d/c/s'


# def test_path_includes_similar_item():
#     path = ':'.join(['/a/b/c', '/a/bd', '/d/c/s'])
#     remove = '/a/b'
#
#     runner = CliRunner()
#     result = runner.invoke(cli, [path, remove])
#     assert result.output == ':'.join(['/a/bd', '/d/c/s'])

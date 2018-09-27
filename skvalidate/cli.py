# -*- coding: utf-8 -*-

"""Console script for skvalidate."""
import os
import sys

import click

plugin_folder = os.path.join(os.path.dirname(__file__), 'commands')


class ValidateCLI(click.MultiCommand):
    """Copied from http://click.pocoo.org/5/commands/#custom-multi-commands."""

    def list_commands(self, ctx):
        """Return a list of available commands."""
        rv = []
        for filename in os.listdir(plugin_folder):
            if filename.endswith('.py'):
                rv.append(filename[:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        """Return the function corresponding to the command."""
        ns = {}
        fn = os.path.join(plugin_folder, name + '.py')
        with open(fn) as f:
            code = compile(f.read(), fn, 'exec')
            eval(code, ns, ns)
        return ns.get('cli', None)


@click.group(cls=ValidateCLI, help='This tool\'s subcommands are loaded from a '
             'plugin folder dynamically.')
def main(args=None):
    """Console script for skvalidate."""
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

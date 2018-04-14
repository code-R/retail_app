"""
rstore

Usage:
  rstore csv_import <csv_file_path>
  rstore -h | --help
  rstore --version

Options:
  -h --help                         Show this screen.
  --version                         Show version.

Examples:
  rstore csv_import

Help:
  This is work in progress
"""


from inspect import getmembers, isclass

from docopt import docopt

VERSION = 1.0

def main():
    """Main CLI entrypoint."""
    from retailstore.cli import commands
    options = docopt(__doc__, version=VERSION)

    # Here we'll try to dynamically match the command the user is trying to run
    # with a pre-defined command class we've already created.

    for k, v in options.items():
        if hasattr(commands, k):
            module = getattr(commands, k)
            commands = getmembers(module, isclass)
            command = [
                command[1]
                for command in commands
                if command[0] != 'Base'
            ][0]

            command = command(options)
            command.run()

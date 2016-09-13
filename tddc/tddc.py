"""Test driven data cleaning
Usage:
  tddc.py summarize <input_file> [--output=<dir>] [--null=<NA>]
  tddc.py build_trello <input_file> [--output=<dir>]
  tddc.py build <input_file> [--output=<dir>]
  tddc.py -h | --help
  tddc.py --version

Options:
  -h --help       Show this screen.
  --version       Show version.
  --output=<dir>  Output directory [default: output]
  --null=<NA>     Null string [default: NA]
"""
from docopt import docopt
from tddc import summarize, build_trello, build
import os
import sys


def get_input_root_dir():
    return os.getcwd()


def get_output_root_dir():
    return os.getcwd()


def execute(cli_args):
    arguments = docopt(__doc__, cli_args, version='TDDC 0.01')
    if arguments['summarize']:
        summarize.go(
            input_root_dir=get_input_root_dir(),
            input_file=arguments['<input_file>'],
            output_root_dir=get_output_root_dir(),
            output_dir=arguments['--output'],
            null_string=arguments['--null'],
        )
    elif arguments['build_trello']:
        build_trello.go(
            summary_root_dir=get_input_root_dir(),
            input_file=arguments['<input_file>'],
            trello_summary_root_dir=get_output_root_dir(),
            output_dir=arguments['--output']
        )
    elif arguments['build']:
        build.go(
            summaries_root_dir=get_input_root_dir(),
            input_file=arguments['<input_file>'],
            scripts_root_dir=get_output_root_dir(),
            output_dir=arguments['--output']
        )


if __name__ == '__main__':
    execute(sys.argv[1:])

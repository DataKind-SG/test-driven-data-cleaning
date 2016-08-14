"""
Common methods used in other modules.
"""
import sys
import os
import json


def get_base_filename(filename):
    """
    Strips out preceding path and file extension from a filename.
    :param filename: Filename, possibly including path and extension.
    :return: Filename without path and without extension.
    """
    base_file = os.path.basename(filename)
    return os.path.splitext(base_file)[0]


def write_summary(summary_data, output_dir, base_name, prefix=''):
    """
    Writes a summary as a json file.
    :param summary_data: a dict containing the summary information.
    :param output_dir: output directory where the summary will be written to.
    :param base_name: common base name for the files.
    :param prefix: a prefix to summary, eg 'trello' or '' for overall summary.
    :return: The full filename (for testing).
    """
    filename = get_summary_filename(output_dir, base_name, prefix)
    with open(filename, 'wt') as writer:
        writer.write(json.dumps(summary_data, allow_nan=True, indent=1))

    print('{} summary of {} is located at: {}'.format(prefix, base_name, filename))
    return filename


def get_summary_filename(output_dir, base_name, prefix=''):
    return os.path.join(output_dir, '{}_{}summary.json'.format(base_name, prefix))


def file_exists_or_exit(filename, message=None):
    """
    Tests if a file exists. Exits if it does not.
    :param filename: Filename to be tested
    :return: None
    """
    if not os.path.isfile(filename):
        print('The file: ' + filename + ' does not exist.')
        print(message)
        sys.exit(1)


def dir_exists_or_make(directory):
    """
    Tests if a directory exists. Makes it if it does not.
    :param directory: Directory to be tested
    :return: None
    """
    if not os.path.isdir(directory):
        os.mkdir(directory)


def read_json_file(filename):
    with open(filename, 'rt') as reader:
        return json.load(reader)


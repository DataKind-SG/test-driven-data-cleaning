import os
try:
    from functools import lru_cache
except ImportError:
    from backports.functools_lru_cache import lru_cache

from tddc import common


def go(summaries_root_dir, input_file, scripts_root_dir, output_dir):
    t = Scripts(summaries_root_dir=summaries_root_dir,
                input_file=input_file,
                scripts_root_dir=scripts_root_dir,
                output_dir=output_dir)
    return t.run()


class Scripts(object):
    """
    This reads the summary data from 'tddc summarize' and trello summary data from tddc build_trello
    and generates the Python scripts with method stubs for both cleaning and testing the cleaning.

    Note that the CLI always passes in the current directory for the summaries_root_dir and scripts_root_dir, but
    they need to be separate variables for testing purposes.
    TODO: the trello summary data shouldn't be required
    """
    def __init__(self, summaries_root_dir, input_file, scripts_root_dir, output_dir):
        self._input_file = input_file
        self._summaries_dir = os.path.join(summaries_root_dir, output_dir)
        self._summary = None
        self._trello_summary = None
        self._scripts_dir = os.path.join(scripts_root_dir, output_dir)
        self.set_summary_data()
        self.set_trello_summary_data()

    @property
    @lru_cache()
    def base_name(self):
        return common.get_base_filename(self._input_file)

    @property
    @lru_cache()
    def summary_dir(self):
        if not os.path.isdir(self._summaries_dir):
            print('Invalid output directory at: ' + self._summaries_dir)
        return self._summaries_dir

    @property
    def scripts_dir(self):
        return self._scripts_dir

    def run(self):
        cleaning_filename = self.write_cleaning_script()
        test_cleaning_filename = self.write_test_cleaning_script()
        return cleaning_filename, test_cleaning_filename

    def set_summary_data(self):
        summary_file = common.get_summary_filename(self.summary_dir, self.base_name)
        common.file_exists_or_exit(
            summary_file, 'Please create the summary file with '
                          '"tddc summarize <input_file> [--output=<dir>] [--null=<NA>]".'
        )
        self._summary = common.read_json_file(summary_file)
        print('Retrieved summary data.')

    def set_trello_summary_data(self):
        trello_summary_file = common.get_summary_filename(self.summary_dir, self.base_name, 'trello')
        common.file_exists_or_exit(
            trello_summary_file, 'Please create the Trello summary file with '
                                 '"tddc build_trello <input_file> [--output=<dir>]'
        )
        self._trello_summary = common.read_json_file(trello_summary_file)
        print('Retrieved Trello summary data.')

    def write_cleaning_script(self):
        cleaning_filename = os.path.join(self.scripts_dir, 'clean_{}.py'.format(self.base_name))
        with open(cleaning_filename, 'wt') as writer:
            self.write_cleaning_boilerplate(writer)
            n_cols = len(self._summary['column_names'])
            for i in range(n_cols):
                self.write_cleaning_column_method(writer, i)
            self.write_cleaning_endnotes(writer)
        print('Finished writing scaffold of cleaning script.')
        return cleaning_filename

    @staticmethod
    def write_cleaning_boilerplate(writer):
        boilerplate_list = [
            'import csv',
            '',
            '',
            'def clean_columns(input_file, output_file):',
            '    with open(input_file) as csvfile, open(output_file, \'wt\') as writer:',
            '        reader = csv.DictReader(csvfile)',
            '        column_names = reader.fieldnames',
            '        writer.write(\',\'.join(column_names) + \'\\n\')',
            '',
            '        n_cols = len(column_names)',
            '        column_methods = [globals()[\'clean_col_\' + str(i)] for i in range(n_cols)]',
            '',
            '        for row in reader:',
            '            cleaned_row = list()',
            '            for i in range(n_cols):',
            '                cleaned_row.append(column_methods[i](row[column_names[i]]))',
            '            writer.write(\',\'.join(cleaned_row) + \'\\n\')',
        ]
        writer.write('\n'.join(boilerplate_list))

    def write_cleaning_endnotes(self, writer):
        endnotes_list = [
            '\n\n',
            'if __name__ == \'__main__\':',
            '    clean_columns(\'{}.csv\', \'cleaned_{}.csv\')'.format(self.base_name, self.base_name),
            ''
        ]
        writer.write('\n'.join(endnotes_list))

    def write_cleaning_column_method(self, writer, column_number):
        column_name = self._summary['column_names'][column_number]
        method_list = [
            '\n\n',
            'def clean_col_{}(input_data):'.format(str(column_number)),
            '    """',
            '    Clean values in column: "{}"'.format(column_name),
            '    Trello card: ' + self._trello_summary['card_urls'][column_name],
            '    """',
            '    return input_data'
        ]
        writer.write('\n'.join(method_list))

    def write_test_cleaning_script(self):
        test_cleaning_filename = os.path.join(
            self.scripts_dir, 'test_clean_{}.py'.format(self.base_name))
        with open(test_cleaning_filename, 'wt') as writer:
            self.write_test_cleaning_boilerplate(writer)
            n_cols = len(self._summary['column_names'])
            for i in range(n_cols):
                self.write_test_cleaning_column_method(writer, i)
        print('Finished writing scaffold of test for cleaning script.')
        return test_cleaning_filename

    def write_test_cleaning_boilerplate(self, writer):
        writer.write('import pytest\n')
        writer.write('import clean_' + self.base_name)

    def write_test_cleaning_column_method(self, writer, column_number):
        column_name = self._summary['column_names'][column_number]
        method_list = [
            '\n\n',
            '@pytest.mark.skip',
            'def test_clean_col_{}():'.format(str(column_number)),
            '    """',
            '    Test the cleaning for column: "{}"'.format(column_name),
            '    """',
            '    assert clean_{base}.clean_col_{num}(\'{null_string}\') == \'{null_string}\''.format(
                base=self.base_name, num=column_number, null_string=self._summary['null_string']),
            '    assert False'
        ]
        writer.write('\n'.join(method_list))

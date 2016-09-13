import os
import csv
from collections import Counter
try:
    from functools import lru_cache
except ImportError:
    from backports.functools_lru_cache import lru_cache

from tddc import common


def go(input_root_dir, input_file, output_root_dir, output_dir, null_string):
    s = Summary(input_root_dir=input_root_dir,
                input_file=input_file,
                output_root_dir=output_root_dir,
                output_dir=output_dir,
                null_string=null_string)
    return s.run()


class Summary(object):
    """
    This reads the input data and writes out a summary of the data (in JSON). The summary includes
    counts of the number of numeric values, max, min, mean, etc. It would be easier to use Pandas,
    but it's probably best to avoid the dependency on such a large package for people who are not regular
    Python or Pandas users.

    Note that the CLI always passes in the current directory for the input_root_dir and output_root_dir, but
    they need to be separate variables for testing purposes.
    """
    def __init__(self, input_root_dir, input_file, output_root_dir, output_dir, null_string='NA'):
        self._input_file = os.path.join(input_root_dir, input_file)
        self._output_dir = os.path.join(output_root_dir, output_dir)
        self._null_string = null_string

    @property
    def null_string(self):
        return self._null_string

    @property
    @lru_cache()
    def base_name(self):
        return common.get_base_filename(self.input_file)

    @property
    @lru_cache()
    def input_file(self):
        common.file_exists_or_exit(self._input_file)
        return self._input_file

    @property
    @lru_cache()
    def output_dir(self):
        common.dir_exists_or_make(self._output_dir)
        return self._output_dir

    def run(self):
        raw_data = self.read_data()
        summary_data = self.summarize_data(raw_data)
        return common.write_summary(summary_data, self.output_dir, self.base_name)

    def read_data(self):
        with open(self.input_file) as csvfile:
            reader = csv.DictReader(csvfile)
            column_names = reader.fieldnames
            raw_data = {
                'column_names': column_names,
                'column_data': {column_name: list() for column_name in column_names}
            }
            for row in reader:
                for column_name in column_names:
                    raw_data['column_data'][column_name].append(row[column_name])

        print('Finished reading data.')
        return raw_data

    def summarize_data(self, raw_data):
        summary_data = {
            'file': self.input_file,
            'base': self.base_name,
            'null_string': self.null_string,
            'column_names': raw_data['column_names'],
            'column_summaries': self.summarize_all_columns(raw_data['column_data'])
        }
        print('Finished summarizing data.')
        return summary_data

    def summarize_all_columns(self, columns_data):
        column_summaries = dict()
        for column_name, column_data in columns_data.items():
            column_summaries[column_name] = self.summarize_column(column_name, column_data)
        return column_summaries

    def summarize_column(self, column_name, column_data):
        n_null, n_nonnull = self.count_nulls(column_data)
        numeric_data = get_numeric_data(column_data)
        nonnumeric_nonnull_data = self.get_nonnumeric_nonnull(column_data)
        length_data = get_lengths(nonnumeric_nonnull_data)
        freq_values, freq_counts = get_most_frequent(column_data)

        column_summary = {
            'n_nonnull': n_nonnull,
            'n_null': n_null,
            'n_int': count_ints(numeric_data),
            'n_numeric': len(numeric_data),
            'max': max(numeric_data),
            'min': min(numeric_data),
            'mean': get_mean(numeric_data),
            'n_non_numeric': len(nonnumeric_nonnull_data),
            'n_unique': len(set(column_data)),
            'max_length': max(length_data),
            'mean_length': get_mean(length_data),
            'freq_values': freq_values,
            'freq_counts': freq_counts
        }

        print('Finished summarizing column: ' + str(column_name))
        return column_summary

    def count_nulls(self, column_data):
        n_null = column_data.count(self.null_string)
        n_nonnull = len(column_data) - n_null
        return n_null, n_nonnull

    def get_nonnumeric_nonnull(self, column_data):
        return list(filter(self.is_nonnumeric_nonnull, column_data))

    def is_nonnumeric_nonnull(self, candidate):
        return (not is_numeric(candidate)) and (candidate != self.null_string)


def count_ints(numeric_data):
    return len(list(filter(is_int, numeric_data)))


def is_int(candidate):
    try:
        assert candidate == int(candidate)
        return True
    except (ValueError, AssertionError, OverflowError):
        return False


def get_numeric_data(column_data):
    return [float(x) for x in list(filter(is_numeric, column_data))] or [float('nan')]


def is_numeric(candidate):
    try:
        float(candidate)
        return True
    except ValueError:
        return False


def get_lengths(nonnumeric_data):
    return [len(x) for x in nonnumeric_data] or [float('nan')]


def get_mean(numeric_data):
    try:
        return float(sum(numeric_data)) / len(numeric_data)
    except ZeroDivisionError:
        return float('NaN')


def get_most_frequent(column_data, n_most=5):
    frequent_tuples = Counter(column_data).most_common(n_most)
    values = [x[0] for x in frequent_tuples]
    counts = [x[1] for x in frequent_tuples]
    return values, counts

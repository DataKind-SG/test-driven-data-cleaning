from pytest import fixture
import os
import math

from tddc import summarize, common


@fixture(scope='module')
def column_data():
    return ['1', '3.2e-3', '-3.0', '0.0', 'NULL', '-2.3', 'a', '1a', 'NULL', '-NULL', '3']


@fixture(scope='module')
def summary_class():
    return summarize.Summary('foo', 'bar', 'baz', 'qux', null_string='NULL')


def test_go(fixtures_dir, input_filename, summary_filename, tmpdir, null_string):
    output_file = summarize.go(fixtures_dir, input_filename, tmpdir.strpath, 'output', null_string)
    actual_summary_data = common.read_json_file(output_file)

    expected_summary_data = common.read_json_file(os.path.join(fixtures_dir, summary_filename))

    # the "file" key is a full path to the summary file and can't be tested across different machines
    expected_keys = expected_summary_data.keys()
    assert actual_summary_data.keys() == expected_keys
    for key in expected_keys:
        if key != 'file':
            assert actual_summary_data[key] == expected_summary_data[key]


def test_count_nulls(column_data, summary_class):
    assert summary_class.count_nulls(column_data) == (2, 9)


def test_get_nonnumeric_nonnull(column_data, summary_class):
    assert summary_class.get_nonnumeric_nonnull(column_data) == ['a', '1a', '-NULL']

    all_numeric = summary_class.get_nonnumeric_nonnull([1, 2, 3])
    assert len(all_numeric) == 0


def test_is_nonnumeric_nonnull(summary_class):
    assert summary_class.is_nonnumeric_nonnull('foo')
    assert summary_class.is_nonnumeric_nonnull('-NULL')
    assert not summary_class.is_nonnumeric_nonnull('NULL')
    assert not summary_class.is_nonnumeric_nonnull('1')
    assert not summary_class.is_nonnumeric_nonnull('2.1')
    assert not summary_class.is_nonnumeric_nonnull('-1.3e4')


def test_is_numeric():
    assert summarize.is_numeric('1.2')
    assert summarize.is_numeric('0')
    assert summarize.is_numeric('-1.4')
    assert not summarize.is_numeric('foo')


def test_is_int():
    assert summarize.is_int(1)
    assert summarize.is_int(-2)
    assert summarize.is_int(0)
    assert not summarize.is_int(1.2)
    assert not summarize.is_int('foo')
    assert not summarize.is_int(float('inf'))


def test_get_numeric_data(column_data):
    assert summarize.get_numeric_data(column_data) == [1, 3.2e-3, -3, 0, -2.3, 3]

    no_numeric = summarize.get_numeric_data(['asdf', 'NULL'])
    assert len(no_numeric) == 1
    assert math.isnan(no_numeric[0])


def test_lengths(summary_class):
    assert summarize.get_lengths(['a', '1a', '-NULL']) == [1, 2, 5]
    no_lengths = summarize.get_lengths(summary_class.get_nonnumeric_nonnull([1, 2, 3, 'NULL']))
    assert math.isnan(summarize.get_mean(no_lengths))
    assert math.isnan(max(no_lengths))


def test_get_mean():
    assert summarize.get_mean([1, 2, 3, 4]) == 2.5
    assert summarize.get_mean([-1.2, 1.2]) == 0
    assert math.isnan(summarize.get_mean([]))
    assert math.isnan(summarize.get_mean([float('nan')]))


def test_get_most_frequent():
    # TODO: this demos the function, but is not really desirable behaviour.
    # Should trim beginning and ending white space at some point.
    values, counts = summarize.get_most_frequent(['1', '1 ', '1'])
    assert values == ['1', '1 ']
    assert counts == [2, 1]

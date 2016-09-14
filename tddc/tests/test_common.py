import pytest
import os

from tddc import common


def test_get_base_filename():
    assert common.get_base_filename('/Users/foo/bar.txt') == 'bar'
    assert common.get_base_filename('bar.txt') == 'bar'
    assert common.get_base_filename('bar') == 'bar'
    assert common.get_base_filename('bar.txt.gz') == 'bar.txt'


def test_write_summary(tmpdir):
    summary_data = {'a': 1, 'b': {'c': 2, 'd': 3}, 'e': [1, 2, 3]}
    filename = common.write_summary(summary_data, tmpdir.strpath, 'foo', 'bar')
    assert os.path.basename(filename) == 'foo_barsummary.json'

    summary_data_from_file = common.read_json_file(filename)
    assert summary_data_from_file == summary_data


def test_file_exists_or_exit():
    with pytest.raises(SystemExit) as exception_info:
        common.file_exists_or_exit('foo.bar.baz')
    assert exception_info.value.code == 1

    assert common.file_exists_or_exit(__file__) is None

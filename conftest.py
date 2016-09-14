from pytest import fixture
import os


@fixture(scope='session')
def fixtures_dir():
    return os.path.join(os.path.dirname(__file__), 'tddc', 'tests', 'fixtures')


@fixture()
def input_filename():
    return 'foo_data.csv'


@fixture()
def summary_filename():
    return 'foo_data_summary.json'


@fixture()
def trellosummary_filename():
    return 'foo_data_trellosummary.json'


@fixture()
def null_string():
    return 'NA'

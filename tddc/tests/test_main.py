import pytest
import os
from mock import patch

from tddc import __main__, common


@pytest.fixture(scope='module')
def root_dir():
    return os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


def test_get_input_root_dir(root_dir):
    assert __main__.get_input_root_dir() == root_dir


def test_get_output_root_dir(root_dir):
    assert __main__.get_output_root_dir() == root_dir


@patch('tddc.__main__.get_input_root_dir')
@patch('tddc.__main__.get_output_root_dir')
def test_cli_summarize(
        mock_output_root_dir, mock_input_root_dir, fixtures_dir, input_filename, null_string, tmpdir
):
    expected_output_loc = common.get_summary_filename(tmpdir.strpath, common.get_base_filename(input_filename))

    output_dir = ''
    cli_args = [
        'summarize', input_filename,
        '--output', output_dir,
        '--null', null_string
    ]
    mock_input_root_dir.return_value = fixtures_dir
    mock_output_root_dir.return_value = tmpdir.strpath

    # test_summarize.py already tests the content of the file. This just tests that the CLI works properly and
    # generates a file at the expected location.
    assert not os.path.isfile(expected_output_loc)
    __main__.execute(cli_args)
    assert os.path.isfile(expected_output_loc)


@patch('tddc.__main__.get_input_root_dir')
@patch('tddc.__main__.get_output_root_dir')
@patch('tddc.build_trello.Trello.client')
def test_cli_build_trello(
        mock_client, mock_output_root_dir, mock_input_root_dir, fixtures_dir, input_filename, tmpdir
):
    expected_output_loc = common.get_summary_filename(
        tmpdir.strpath, common.get_base_filename(input_filename), 'trello')

    output_dir = ''
    cli_args = [
        'build_trello', input_filename,
        '--output', output_dir
    ]

    mock_input_root_dir.return_value = fixtures_dir
    mock_output_root_dir.return_value = tmpdir.strpath
    mock_client.add_board().url = 'MOCK_BOARD_URL'
    mock_client.add_board().add_list().add_card().url = 'MOCK_CARD_URL'

    # test_build_trello.py already tests the content of the file. This just tests that the CLI works properly and
    # generates a file at the expected location.
    assert not os.path.isfile(expected_output_loc)
    __main__.execute(cli_args)
    assert os.path.isfile(expected_output_loc)

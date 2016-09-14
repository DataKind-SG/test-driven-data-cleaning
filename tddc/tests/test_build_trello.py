import os
from mock import patch

from tddc import build_trello, common


@patch('tddc.build_trello.Trello.client')
def test_go(mock_client, fixtures_dir, input_filename, trellosummary_filename, tmpdir):
    mock_client.add_board().url = 'MOCK_BOARD_URL'
    mock_client.add_board().add_list().add_card().url = 'MOCK_CARD_URL'
    output_filename = build_trello.go(fixtures_dir, input_filename, tmpdir.strpath, '')
    actual_summary_data = common.read_json_file(output_filename)
    # TODO: add asserts on mock calls

    expected_summary_data = common.read_json_file(os.path.join(fixtures_dir, trellosummary_filename))
    assert actual_summary_data == expected_summary_data

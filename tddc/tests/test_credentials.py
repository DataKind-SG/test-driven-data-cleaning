from mock import patch

from tddc import credentials


@patch('tddc.credentials.os.path.expanduser')
@patch('tddc.credentials.TrelloClient')
def test_go(mock_trello_client, mock_expanduser, fixtures_dir):
    mock_expanduser.return_value = fixtures_dir
    credentials.TrelloConnector().get_client()
    mock_trello_client.assert_called_once_with(api_key='foo', token='bar')
    mock_trello_client.return_value.list_hooks.assert_called_once_with('bar')

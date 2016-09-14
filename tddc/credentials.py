import os
import sys
import yaml
try:
    from functools import lru_cache
except ImportError:
    from backports.functools_lru_cache import lru_cache

from trello import TrelloClient, Unauthorized


class TrelloConnector(object):
    """
    Retrieves trello credentials if they exist.
    TODO: creates trello credentials if they don't exist.
    Tests and returns a connection to Trello.
    """
    def __init__(self):
        self._api_key = None
        self._token = None

    def _set_creds(self):
        config_file = os.path.join(os.path.expanduser('~'), '.tddc_config.yml')
        if not os.path.isfile(config_file):
            print('Trello configuration file not found at ' + config_file)
            self._write_config()

        while self._api_key is None or self._token is None:
            try:
                with open(config_file, 'rt') as ymlfile:
                    config = yaml.load(ymlfile)
                self._extract_config(config)
            except:
                print('Invalid yaml file.')
                self._write_config()

    def _extract_config(self, config):
        try:
            self._api_key = config['trello']['api_key']
            self._token = config['trello']['token']
        except KeyError:
            print('Invalid trello configuration file.')
            self._write_config()

    @lru_cache()
    def get_client(self):
        client = None
        while client is None:
            self._set_creds()
            client = TrelloClient(api_key=self._api_key, token=self._token)
            try:
                client.list_hooks(self._token)
            except Unauthorized:
                print('Trello client is not authorized.')
                client = None
                self._write_config()

        print('Trello client successfully authorized.')
        return client

    @staticmethod
    def _write_config():
        print('TrelloCredentials._write_configuration not yet implemented. For now, you can create a file '
              '.tddc_config.yml in the user root directory with the format:')
        print(' ')
        print('trello:')
        print('    api_key: <TRELL_API_KEY>')
        print('    token: <TRELLO_TOKEN>')
        print(' ')
        print('You can get your Trello API key here: https://trello.com/app-key')
        print('and your Trello token here: https://trello.com/1/authorize?expiration=1day&'
              'scope=read,write,account&response_type=token&name=Server%20Token&key=<TRELLO_API_KEY>')
        sys.exit(1)

import os
try:
    from functools import lru_cache
except ImportError:
    from backports.functools_lru_cache import lru_cache

from tddc import common
from tddc.credentials import TrelloConnector


def go(summary_root_dir, input_file, trello_summary_root_dir, output_dir):
    t = Trello(summary_root_dir=summary_root_dir,
               input_file=input_file,
               trello_summary_root_dir=trello_summary_root_dir,
               output_dir=output_dir)
    return t.run()


class Trello(object):
    """
    This reads the summary data from 'tddc summarize' and populates a Trello board with a card
    for each column containing summary information in the card description.

    Note that the CLI always passes in the current directory for the summary_root_dir and trello_summary_root_dir, but
    they need to be separate variables for testing purposes.
    """
    def __init__(self, summary_root_dir, input_file, trello_summary_root_dir, output_dir):
        self._input_file = input_file
        self._summary_dir = os.path.join(summary_root_dir, output_dir)
        self._summary = None
        self._trello_summary_dir = os.path.join(trello_summary_root_dir, output_dir)
        self._trello_summary = dict()
        self._board = None
        self._backlog_list = None

    @property
    @lru_cache()
    def client(self):
        return TrelloConnector().get_client()

    @property
    @lru_cache()
    def base_name(self):
        return common.get_base_filename(self._input_file)

    @property
    @lru_cache()
    def summary_dir(self):
        if not os.path.isdir(self._summary_dir):
            print('Invalid output directory at: ' + self._summary_dir)
        return self._summary_dir

    @property
    def trello_summary_dir(self):
        return self._trello_summary_dir

    def run(self):
        self.set_summary_data()
        self.add_board()
        self.add_lists()
        self.add_cards()
        return common.write_summary(self._trello_summary, self.trello_summary_dir, self.base_name, 'trello')

    def set_summary_data(self):
        summary_file = common.get_summary_filename(self.summary_dir, self.base_name)
        common.file_exists_or_exit(
            summary_file, 'Please create the summary file with '
                          '"tddc summarize <input_file> [--output=<dir>] [--null=<NA>]".'.format(summary_file)
        )
        self._summary = common.read_json_file(summary_file)
        print('Retrieved summary data.')

    def add_board(self):
        board_title = 'Data Cleaning Board for: ' + self.base_name
        self._board = self.client.add_board(board_title)
        for trello_lists in self._board.get_lists('all'):
            trello_lists.close()

        print('Created Trello board: "{}" at: {}'.format(board_title, self._board.url))
        self._trello_summary['board'] = {
            'title': board_title,
            'url': self._board.url
        }

    def add_lists(self):
        self._board.add_list('Accepted')
        self._board.add_list('For Review')
        self._board.add_list('In Progress')
        self._backlog_list = self._board.add_list('Backlog')
        print('Created lists: "Backlog", "In Progress", "For Review" and "Accepted"')

    def add_cards(self):
        column_names = self._summary['column_names']
        n_columns = len(column_names)
        self._trello_summary['card_urls'] = dict()

        for i in range(n_columns):
            column_name = column_names[i]
            card_name = 'Column: ' + column_name
            column_summary = self._summary['column_summaries'][column_name]
            description = [
                'Method: `process_col_{}`, Test method: `test_process_col_{}`.\n'.format(i, i),
                '- number of non-null rows: **{}**'.format(column_summary['n_nonnull']),
                '- number  of null rows: **{}**'.format(column_summary['n_null']),
                '- number of numeric rows: **{}**'.format(column_summary['n_numeric']),
                '- max of numeric rows: **{}**'.format(column_summary['max']),
                '- min of numeric rows: **{}**'.format(column_summary['min']),
                '- mean of numeric rows: **{}**\n'.format(column_summary['mean']),
                '- number of non-numeric rows: **{}**'.format(column_summary['n_non_numeric']),
                '- max length of non-numeric rows: **{}**'.format(column_summary['max_length']),
                '- mean length of non-numeric rows: **{}**\n'.format(column_summary['mean_length']),
                'Most frequent values [value: count]\n'
            ]
            for j in range(len(column_summary['freq_values'])):
                description.append(
                    '- `{}`: **{}**'.format(column_summary['freq_values'][j], column_summary['freq_counts'][j]))

            card = self._backlog_list.add_card(card_name, desc='\n'.join(description))
            self._trello_summary['card_urls'][column_name] = card.url
            print('Created card: "{}"'.format(card_name))

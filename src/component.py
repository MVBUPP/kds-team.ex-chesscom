"""
Template Component main class.

"""
import csv
import logging
from datetime import datetime

from keboola.component.base import ComponentBase
from keboola.component.exceptions import UserException

# configuration variables
KEY_API_TOKEN = '#api_token'
KEY_PRINT_HELLO = 'print_hello'

# list of mandatory parameters => if some is missing,
# component will fail with readable message on initialization.
REQUIRED_PARAMETERS = [KEY_PRINT_HELLO]
REQUIRED_IMAGE_PARS = []


class Component(ComponentBase):
    """
        Extends base class for general Python components. Initializes the CommonInterface
        and performs configuration validation.

        For easier debugging the data folder is picked up by default from `../data` path,
        relative to working directory.

        If `debug` parameter is present in the `config.json`, the default logger is set to verbose DEBUG mode.
    """

    def __init__(self):
        super().__init__()

    def run(self):
        """
        Main execution code
        """
        # Get user configuration
        # Fetch data from Chess.com API
        # https://api.chess.com/pub/player/magsstrats/stats

        
        from chessdotcom import get_player_stats, Client
        Client.request_config["headers"]["User-Agent"] = (
            "My Python Application. "
            "Contact me at mvbupp@gmail.com"
        )
        response = get_player_stats('magsstrats')
        print(response.json)
        player_name = "magsstrats"

        data = response.json
        categories=['chess_blitz', 'chess_bullet', 'chess_rapid']
        

        #output_table_path = self.create_out_table_definition('chess_stats.csv').full_path
        output_table_path='chess_stats.csv'
        # Write data to output table
        with open(output_table_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Define column headers based on the data structure
            writer.writerow(
                ['username', 'category', 'rating'])

            # Parse and write data rows
            for category in categories:
                writer.writerow([
                    player_name,
                    category,
                    data['stats'][category]['last']['rating'],
                ])

        # Log completion message
        #self.logger.info(f'Data for user {player_name} fetched successfully.')

if __name__ == "__main__":
    try:
        comp = Component()
        # this triggers the run method by default and is controlled by the configuration.action parameter
        comp.execute_action()
    except UserException as exc:
        logging.exception(exc)
        exit(1)
    except Exception as exc:
        logging.exception(exc)
        exit(2)

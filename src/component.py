"""
Template Component main class.

"""
import csv

import logging
from datetime import datetime

from keboola.component.base import ComponentBase
from keboola.component.exceptions import UserException
# Load the Component library to process the config file
from keboola.component import CommonInterface
#os.chdir("./data")
# Rely on the KBC_DATADIR environment variable by default,
# alternatively provide a data folder path in the constructor (CommonInterface('data'))
#ci = CommonInterface('data')



# configuration variables
KEY_API_TOKEN = '#api_token'


# list of mandatory parameters => if some is missing,
# component will fail with readable message on initialization.
REQUIRED_PARAMETERS = []
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
        params = self.configuration.parameters
        PLAYER_NAME = params['player_name']
        LEADERBOARDS= params['leaderboard_type']
        def get_chess_leaderboards():
            response=get_leaderboards()
            

            data = response.json
            
            
            #comment
            categories=data.keys()
            subcategories=LEADERBOARDS
            if("all" in LEADERBOARDS):
                subcategories=data.keys()
                
            #output_table_path='./out/tables/chess_leaderboards.csv'
            table = self.create_out_table_definition('chess_leaderboards.csv', incremental= True)
            #output_path=table.full_path
            #write data
            #write data
            with open(table.full_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                # Define column headers based on the data structure

                # Parse and write data rows
                for category in categories:
                        for entry1 in subcategories:
                            
                            writer.writerow(['Category','Rank', 'Username', 'Score'])
                            for entry in data[category][entry1]:
                                writer.writerow([
                                    entry1,
                                    entry['rank'],
                                    entry['username'],
                                    entry['score']
                                ])

        #output_table_path = self.create_out_table_definition('chess_stats.csv').full_path
        def get_chess_stats_player(player_name):
            response = get_player_stats(player_name)
            categories=['chess_blitz', 'chess_bullet', 'chess_rapid']
            #output_table_path='./out/tables/chess_stats.csv'
            output_table_path = self.create_out_table_definition('chess_stats.csv', incremental=True).full_path
            data = response.json
            #write data
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

        from chessdotcom import get_player_stats, Client, get_leaderboards
        Client.request_config["headers"]["User-Agent"] = (
            "My Python Application. "
            "Contact me at mvbupp@gmail.com"
        )
        
        get_chess_leaderboards()
        get_chess_stats_player(PLAYER_NAME)

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

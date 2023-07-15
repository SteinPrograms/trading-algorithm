"""This is the brokerage connection module


It contains the following methods :
- test_order (check connection to the broker)
- get_order_status (check if order is filled)
- get_balances (get the current balances to place order)
- place_order (place an order)
"""


# Imports from standard library
from dotenv import load_dotenv

# Imports from local packages
from broker import settings
from binance.spot import Spot


class BinanceCommands():

    def __init__(self):
        """Initiate the connection to the broker"""
        self.client = Spot(settings.API_KEY, settings.API_SECRET)

    def test_order(self):
        """Test the connection to the broker"""
        return self.client.account_status()



BinanceCommands().test_order()
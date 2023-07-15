"""Brokerage connection module

It contains the following methods :
- test_order (check connection to the broker)
- get_order_status (check if order is filled)
- get_balances (get the current balances to place order)
- place_order (place an order)
"""

# Imports from standard library
import os
import dataclasses
from dotenv import load_dotenv

# Imports from local packages
from binance.spot import Spot
from binance.error import ClientError



class BinanceCommands():
    """Binance SDK"""

    @dataclasses.dataclass
    class Order:
        """ORDER CONSTRUCTOR"""
        open_price : float

    def __init__(self):
        """Initiate the connection to the broker"""
        load_dotenv()
        # Read API keys from environment variables
        api_key = os.environ.get('API_KEY')
        api_secret = os.environ.get('API_SECRET')
        self.client = Spot(api_key, api_secret)

    def test_connection(self):
        """Test the connection to the broker"""
        try:
            self.client.account_status()
            return True
        except ClientError:
            return False

    def get_order_status(self, order_id):
        """Check if order is filled"""
        return self.client.get_order(symbol="BTCUSDT", orderId=order_id)

    def get_balances(self):
        """Get the current balances to place order"""
        self.client.get_open_orders()
        return self.client.account_snapshot(
            type="SPOT",
        ).get("snapshotVos")[0].get("data").get("balances")

    def market_open(self, symbol) -> Order:
        """Place an order"""
        return self.client.new_order(
            symbol=symbol,
            side="BUY",
            type="MARKET",
            quantity="0.001")

    def market_close(self, symbol):
        """Place an order"""
        return self.client.new_order(
            symbol=symbol,
            side="SELL",
            type="MARKET",
            quantity="0.001")

from pprint import pprint
pprint(BinanceCommands().get_balances())

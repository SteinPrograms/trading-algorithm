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
        price : float
        order_id : str
        def __init__(price:float,order_id:str):
            self.price = price
            self.order_id = order_id

    def __init__(self,backtesting):
        """Initiate the connection to the broker"""
        if backtesting:
            self.client = Spot()
            self.backtesting = backtesting
            return
        load_dotenv()
        # Read API keys from environment variables
        api_key = os.environ.get('API_KEY')
        private_key = os.environ.get('API_SECRET')
        with open(private_key, 'rb') as f:
            private_key = f.read()
        self.client = Spot(api_key = api_key, private_key=private_key)

    def test_connection(self):
        """Test the connection to the broker"""
        try:
            self.client.account_status()
            return True
        except ClientError:
            return False

    def get_order_status(self, symbol, order_id):
        """Check if order is filled"""
        return self.client.get_order(symbol=symbol, orderId=order_id)

    def get_balances(self):
        """Get the current balances"""
        return self.client.user_asset()

    def get_balance(self, asset)->float:
        """Get the current balance of asset to place order"""
        return self.client.user_asset(asset=asset)[0]

    def market_open(self, quote,asset) -> Order:
        """Place an order"""
        if self.backtesting:
            return Order(price=self.get_prices(asset,quote))

        quantity,_ = self.calculate_order_parameters(quote=quote,asset=asset)


        return self.client.new_order(
            symbol=f"{asset}{quote}",
            side="BUY",
            type="MARKET",
            quantity=quantity,
            newClientOrderId = "open",
        )

    def market_close(self, quote,asset) -> Order:
        """Place an order"""

        # Calculate the quantity from balance (only use 99% of available balance)
        _,quantity = self.calculate_order_parameters(quote=quote,asset=asset)
        print("quantity",quantity)
        return self.client.new_order(
            symbol=f"{asset}{quote}",
            side="SELL",
            type="MARKET",
            quantity=quantity,
            newClientOrderId = "close",
        )

    def get_fee(self,symbol:str=None):
        """Get the current fee"""
        if symbol:
            return self.client.trade_fee(symbol=symbol)
        return self.client.trade_fee()

    def calculate_order_parameters(self,*,quote:str,asset:str=None):
        """Calculate the buying power from the balance"""
        prices = self.get_prices(asset=asset,quote=quote)
        balances = self.get_balances()
        for balance in balances:
            if balance.get("asset") == quote:
                balance_quote = float(balance.get("free"))
            if balance.get("asset") == asset:
                balance_asset = float(balance.get("free"))
        
        for _filter in self.get_precision(asset=asset,quote=quote).get("filters"):
            if _filter.get("filterType") == "LOT_SIZE":
                step_size = _filter.get("stepSize")
                precision = step_size.find('1')-1
                break
        
        precisions = self.get_precision(asset=asset,quote=quote).get("filters")
        precision_quote,precision_asset = precisions.get("quoteAssetPrecision"),precisions.get('baseAssetPrecision')
        
        quantity_quote = round(float((balance_quote))/float(prices.get("bidPrice")),precision_asset)
        quantity_asset = float(str(balance_asset)[:2+precision])
        return quantity_quote,quantity_asset

    def get_prices(self,asset,quote):
        """Get the current price"""
        return self.client.book_ticker(symbol=f"{asset}{quote}")

    def get_precision(self,*,asset,quote):
        """Get the precision of the asset"""
        return self.client.exchange_info(symbol=f"{asset}{quote}").get("symbols")[0]

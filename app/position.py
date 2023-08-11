"""Module used for position management"""


import time
import dataclasses
import requests
from datetime import datetime
from database import Database
from prediction import Prediction

@dataclasses.dataclass
class Prices:
    """Differents prices used to monitor position
    """
    open : float = None
    close : float = None
    highest : float = None
    lowest : float = None
    take_profit : float = None
    stop_loss : float = None
    current : float = None

@dataclasses.dataclass
class Times:
    """Differents prices used to monitor position
    """
    open : datetime = None
    close : datetime = None

@dataclasses.dataclass
class Settings:
    """Differents prices used to monitor position
    """
    status : str = 'close'
    quote : str = 'USDT'
    asset : str = 'BTC'
    symbol : str = asset+quote
    fee : float = 0.1/100
    risk : float = 0.5/100
    exit_mode : str = None
    backtesting : bool = True


class Position:
    """This class is used to store all the data used to create orders and to make the calculation.
    Defaults : backtesting is True and symbol is 'BTC'
    """
    def __init__(self):
        self.settings = Settings()
        self.prices = Prices()
        self.times = Times()

    def update_price(self):
        """
        {
            "symbol": "LTCBTC",
            "price": "4.00000200"
        }
        """
        price = requests.get('https://data-api.binance.vision/api/v3/ticker/price',params={
            'symbol':'BTCUSDT',
        })
        self.prices.current = float(price.json().get('price'))

    def open_position(self):
        """This function send an open order to the broker, with the opening price,
        and then save the data inside the class Position.
        """

        # Setting highest price and lowest price to the opening price
        self.prices.open,self.prices.highest,self.prices.lowest = prices.current
        # Changing status to open
        self.settings.status = 'open'
        self.times.open = time.time()

        return open_order


    def close_position(self):
        """This function send a close market order to the broker
        save the database inside the database
        """

        self.settings.status = 'close'
        self.times.close = time.time()
        return close_order

    def monitor_position(self):
        """
        Start a new thread that will monitor the position
        """
        # Updating current price
        self.update_price()

        # Updating highest_price
        if self.prices.current > self.prices.highest:
            self.prices.highest = self.prices.current

        # Updating lowest_price
        if self.prices.current < self.prices.lowest:
            self.prices.lowest = self.prices.current

        # Calculating current effective_yield
        effective_yield = self.effective_yield_calculation(
            current_price=self.prices.current,
            opening_price=self.prices.open,
            fee=self.settings.fee,
        )

        # Stop loss
        # Close position :
        if effective_yield < self.settings.risk:
            self.prices.close = self.prices.open * self.settings.risk
            self.settings.exit_mode = "stop-loss"
            self.close_position()
            return

        # Take profit
        # Closing on take-profit :
        #   -> Check if the yield  is stronger  than the minimal yield considering fees and slippage
        if self.prices.current > self.prices.take_profit :
            self.prices.close = self.prices.current
            self.settings.exit_mode = "take-profit"
            self.close_position()
            return
    
        # Closing on sell signal :
        #   -> Check if signal is sell
        if Prediction().signal(self.settings.symbol) == 'sell' :
            self.prices.close = self.prices.current
            self.settings.exit_mode = "sell-signal"
            self.close_position()
            return


    def effective_yield_calculation(self,current_price, opening_price, fee):
        """Calculate the real yield considering fees and current price"""
        return_on_investment = float(current_price) / float(opening_price)
        fee = float(fee)
        return (return_on_investment - (
            fee + (1 - fee) * return_on_investment * fee
            )
        )

if __name__ == '__main__':
    print(Position().prices)
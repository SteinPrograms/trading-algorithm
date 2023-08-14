"""Module used for position management"""


import time
import dataclasses
import requests
from datetime import datetime
from database import Database
from prediction import Prediction
from log import Log

@dataclasses.dataclass
class Prices:
    """Differents prices used to monitor position
    """
    open : float = 0.0
    close : float = 0.0
    highest : float = 0.0
    lowest : float = 0.0
    current : float = 0.0

@dataclasses.dataclass
class Times:
    """Differents prices used to monitor position
    """
    open : datetime = datetime.now()
    close : datetime = datetime.now()

@dataclasses.dataclass
class Settings:
    """Differents prices used to monitor position
    """
    id : int = 0
    status : str = 'close'
    quote : str = 'USDT'
    asset : str = 'BTC'
    symbol : str = asset+quote
    fee : float = 0.1/100
    stop_loss : float = 0.5/100
    take_profit : float = 0.2/100
    exit_mode : str = 'default'


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
        if price.status_code != 200:
            Log(f"Error {price.status_code} while updating price")
            return
        self.prices.current = float(price.json().get('price'))
        

    def open_position(self):
        """This function send an open order to the broker, with the opening price,
        and then save the data inside the class Position.
        """

        self.settings.id += 1
        # Setting highest price and lowest price to the opening price
        self.prices.open = self.prices.highest = self.prices.lowest = self.prices.current
        print(self.prices)
        # Changing status to open
        self.settings.status = 'open'
        self.times.open = datetime.now()
        Log("Opening position")
        return


    def close_position(self):
        """This function send a close market order to the broker
        save the database inside the database
        """

        self.settings.status = 'close'
        self.times.close = datetime.now()
        Log("Closing position")
        return

    def monitor_position(self,predictor:Prediction):
        """
        Start a new thread that will monitor the position
        """
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
        if effective_yield <= 1-self.settings.stop_loss:
            self.prices.close = self.prices.open * (1-self.settings.stop_loss)
            self.settings.exit_mode = "stop-loss"
            self.close_position()
            return

        # Take profit
        # Closing on take-profit :
        #   -> Check if the yield  is stronger  than the minimal yield considering fees and slippage
        if effective_yield >= 1+self.settings.take_profit :
            self.prices.close = self.prices.open * (1+self.settings.take_profit)
            self.settings.exit_mode = "take-profit"
            self.close_position()
            return
    
        # Closing on sell signal :
        #   -> Check if signal is sell
        if predictor.signal(self.settings.symbol) == 'sell' :
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
    print(Position().effective_yield_calculation(current_price=20000,opening_price=21000,fee=0.1/100))
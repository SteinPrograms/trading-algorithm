"""Module used for position management"""

import time
import dataclasses
from datetime import datetime
from indicator import Indicator

def effective_yield_calculation(current_price, opening_price, fee):
    """
    Computes yield considering fees and current price
    """
    return_on_investment = float(current_price) / float(opening_price)
    fee = float(fee)
    return (return_on_investment - (
        fee + (1 - fee) * return_on_investment * fee
        )
    )

@dataclasses.dataclass
class Prices:
    """
    Differents prices of the positions 
    -> could be visualized as a kline
    """
    open : float = 0.0
    close : float = 0.0
    highest : float = 0.0
    lowest : float = 0.0
    current : float = 0.0

@dataclasses.dataclass
class Times:
    """
    Times of the position
    """
    open : datetime = datetime.now()
    close : datetime = datetime.now()

@dataclasses.dataclass
class Settings:
    """
    Settings of the position
    """
    id : int = 0
    status : 'close' or 'open' = 'close'
    quote : str = 'USDT'
    asset : str = 'BTC'
    symbol : str = asset+quote
    fee : float = 0.1/100
    stop_loss : float = 2/100
    take_profit : float = 0.5/100
    exit_mode : str = 'default'
    trailing_stop_loss : float = 0.1/100
    realized_yield : float = 0.0


class Position:
    """
    A position is a trade
    """
    def __init__(self):
        self.settings = Settings()
        self.prices = Prices()
        self.times = Times()        

    def open_position(self):
        """
        Sends market order to the broker
        Register the opening price and time
        Update the status to open
        """
        self.settings.id += 1
        # Setting highest price and lowest price to the opening price
        self.prices.open = self.prices.highest = self.prices.lowest = self.prices.current
        # Changing status to open
        self.settings.status = 'open'
        self.times.open = datetime.now()
        return


    def close_position(self):
        """
        Sends market order to the broker
        Register the closing time
        """
        self.settings.realized_yield = effective_yield_calculation(
            current_price=self.prices.close,
            opening_price=self.prices.open,
            fee=self.settings.fee,
        )
        self.settings.status = 'close'
        self.times.close = datetime.now()
        return

    def monitor_position(self,indicator:Indicator):
        """
        Updates prices
        Checks if stop loss or take profit is reached
        """
        # Updating highest_price
        if self.prices.current > self.prices.highest:
            self.prices.highest = self.prices.current

        # Updating lowest_price
        if self.prices.current < self.prices.lowest:
            self.prices.lowest = self.prices.current

        # Compute realtime yield (without fees)
        computed_yield = self.prices.current / self.prices.open

        # Stop loss
        # Close position :
        if computed_yield <= 1-self.settings.stop_loss:
            self.prices.close = self.prices.open * (1-self.settings.stop_loss)
            self.settings.exit_mode = "stop-loss"
            self.close_position()
            return

        # Take profit
        # Closing on take-profit :
        # -> Once we pass the take profit threshold, we add a trailing stop loss (of X% which increase with the price)
        if self.prices.highest / self.prices.open >= 1+self.settings.take_profit :
            if self.prices.current / self.prices.highest <= 1-self.settings.trailing_stop_loss:
                self.prices.close = self.prices.highest * (1-self.settings.trailing_stop_loss)
                self.settings.exit_mode = "take-profit"
                self.close_position()
                return
    
        # Closing on sell signal :
        #   -> Check if signal is sell
        if indicator.signal == 'sell' :
            self.prices.close = self.prices.current
            self.settings.exit_mode = "sell-signal"
            self.close_position()
            return

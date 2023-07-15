"""Module used for position management"""


import time

from database import Database
from bot_exceptions import DatabaseException
from broker import BinanceCommands

class Position:
    """This class is used to store all the data used to create orders and to make the calculation.
    Defaults : backtesting is True and symbol is 'BTC'
    """
    def __init__(self,*,backtesting : bool = True,symbol : str = 'BTC',database: Database):
        self.symbol = f'{symbol}/{settings.BASE_ASSET}'
        self.status='close'
        self.effective_yield = 1 # Yield considering fees and slippage
        self.highest_yield=1 # Highest yield reached
        self.open_price = None
        self.close_price = None
        self.current_price = None
        self.highest_price = None
        self.lowest_price = None
        self.close_mode = None
        self.opening_time = None

    def open_position(self):
        """This function send an open order to the broker, with the opening price,
        and then save the data inside the class Position.
        """
        # Create a new order at market price
        order = BinanceCommands().market_open(self.symbol)
        # Setting highest price and lowest price to the opening price
        self.open_price,self.highest_price,self.lowest_price = order.open_price
        # Changing status to open
        self.status = 'open'
        self.opening_time = time.time()

        return order


    def close_position(self):
        """This function send a close market order to the broker
        save the database inside the database
        """

        BinanceCommands().market_close(self.symbol)

        self.status = 'close'
        self.effective_yield = self.effective_yield_calculation(
                                    self.close_price,
                                    self.open_price,
                                    settings.FEE,
                                )


    def force_position_close(self):
        """Force position to close at marketprice"""
        self.close_price = self.current_price
        if not self.backtesting:
            order = RealCommands().market_close(self.symbol, backtesting=self.backtesting)
            logger.debug(order)
        self.close_mode = "force-close"
        self.close_position()


    def monitor_position(self):
        """
        Start a new thread that will monitor the position
        """

        # Updating highest_price
        if self.current_price > self.highest_price:
            self.highest_price = self.current_price

        # Updating lowest_price
        if self.current_price < self.lowest_price:
            self.lowest_price = self.current_price

        # Calculating current effective_yield
        self.effective_yield = self.effective_yield_calculation(
                                            current_price=self.current_price,
                                            opening_price=self.open_price,
                                            fee=settings.FEE,
                                        )

        # Stop loss
        # Close position :
        if self.effective_yield < settings.RISK:
            self.close_price = self.open_price * settings.RISK
            if not self.BACKTESTING:
                broker.BinanceCommands().market_close(symbol=self.symbol, backtesting=self.BACKTESTING)
            self.close_mode = "stop-loss"
            self.close_position()
            return

        # Take profit on expected yield
        # Closing on take-profit :
        #   -> Check if the yield  is stronger  than the minimal yield considering fees and slippage
        if self.current_effective_yield > 1+self.expected_yield:
            self.close_price = self.current_price
            if not self.BACKTESTING:
                RealCommands().market_close(symbol=self.symbol, backtesting=self.BACKTESTING)
            self.close_mode = "take-profit"
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

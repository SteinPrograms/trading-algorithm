"""Module used for position management"""

# Standard import
import datetime
import time
from collections import deque

# Local imports
import settings
from database import Database
from brokerconnection import RealCommands
from bot_exceptions import DatabaseException
from local_websocket.websocket_client import FtxWebsocketClient
from logs import logger

class Position:
    """This class is used to store all the data used to create orders and to make the calculation.
    Defaults : backtesting is True and symbol is 'BTC'
    """
    def __init__(self,*,backtesting : bool = True,symbol : str = 'BTC',database: Database):
        self.symbol = f'{symbol}/{settings.BASE_ASSET}'
        self.backtesting = backtesting
        self.current_status='close'
        self.current_effective_yield = 1
        self.highest_yield=1
        self.expected_yield = settings.EXPECTED_YIELD
        self.database = database
        self.identifier = None
        self.open_price = None
        self.current_price = None
        self.highest_price = None
        self.lowest_price = None
        self.opening_time = None
        self.effective_yield = None
        self.total_yield = None
        self.close_mode = None
        self.close_price = None
        self.statistics = {}
        self.decision = "hodle"
        self.websocket = FtxWebsocketClient()
        while True:
            current_data = self.websocket.get_ticker(self.symbol)
            if 'bid' in current_data:
                # Initializing the trigger_price at initialization price
                self.trigger_price = current_data.get('bid')
                logger.info("Initialized price at : %s",self.trigger_price)
                break

    def is_open(self):
        """Return true if position is open"""
        return self.current_status=='open'

    def open_position(self):
        """This function send an open order to the broker, with the opening price,
        and then save the data inside the class Position.
        """
        if not self.backtesting:
            order = RealCommands().market_open(symbol=self.symbol, backtesting=self.backtesting)
            if order['error']:
                return False
            logger.info("Open order success : %s",order)
            self.identifier = order['order']['id']
        else:
            # Simulation of opening position time by broker
            time.sleep(2)
        self.open_price = self.current_price
        # Setting highest price and lowest price to the opening price
        self.highest_price = self.open_price
        self.lowest_price = self.open_price
        self.current_status = 'open'
        self.opening_time = time.time()
        return True


    def close_position(self):
        """This function send a close market order to the broker
        save the database inside the database
        """
        self.current_status = 'close'
        self.effective_yield = self.effective_yield_calculation(
                                    self.close_price,
                                    self.open_price,
                                    settings.FEE,
                                )
        self.total_yield = self.total_yield*self.effective_yield
        if  self.total_yield > self.highest_yield:
            self.highest_yield = self.total_yield

        try:
            if not self.backtesting:
                order_data = RealCommands().get_order_status(self.identifier)
                logger.info("Close order success : %s",order_data)
                self.database.add_position(
                    time=self.opening_time,
                    symbol=self.symbol,
                    yield_value=self.effective_yield,
                    wallet_value=order_data.get('avgFillPrice',0)*order_data.get('filledSize',0),
                )
            else:
                self.database.add_position(
                    time=self.opening_time,
                    symbol=self.symbol,
                    yield_value=self.effective_yield,
                    wallet_value=0,
                )
        except DatabaseException as error:
            logger.error(error)


    def force_position_close(self):
        """Force position to close at marketprice"""
        self.close_price = self.current_price
        if not self.backtesting:
            order = RealCommands().market_close(self.symbol, backtesting=self.backtesting)
            logger.debug(order)
        self.close_mode = "force-close"
        self.close_position()


    def check_position(self):
        """Update the highest_price and the lowest price
        Then checks if it has to close the position
        """

        # Updating highest_price
        if self.current_price > self.highest_price:
            self.highest_price = self.current_price

            # Updating lowest_price
        if self.current_price < self.lowest_price:
            self.lowest_price = self.current_price

            # Calculating current effective_yield
        self.current_effective_yield = self.effective_yield_calculation(
                                            current_price=self.current_price,
                                            opening_price=self.open_price,
                                            fee=settings.FEE,
                                        )

        # Stop loss
        # Close position :
        if self.current_effective_yield < 1-settings.RISK:
            self.close_price = self.open_price * settings.RISK
            if not self.backtesting:
                RealCommands().market_close(self.symbol, backtesting=self.backtesting)
            self.close_mode = "stop-loss"
            self.close_position()
            return

        # Take profit on expected yield and sell decision
        # Closing on take-profit :
        #   -> Check if the yield  is stronger  than the minimal yield considering fees and slippage
        if self.decision == "sell":
            if self.current_effective_yield > 1+self.expected_yield:
                self.close_price = self.current_price
                if not self.backtesting:
                    RealCommands().market_close(symbol=self.symbol, backtesting=self.backtesting)
                self.close_mode = "take-profit"
                self.close_position()
                return

    def manage_position(self):
        """Manage position : look for selling or buying actions"""
        while True:
            current_data = self.websocket.get_ticker(self.symbol)
            if 'bid' in current_data:
                self.current_price = current_data.get('bid')
                break


        self.statistics['symbol'] = self.symbol
        self.statistics['current_price'] = self.current_price
        self.statistics['current_status'] = self.current_status
        self.statistics['total_yield'] = self.total_yield
        self.statistics['decision'] = self.decision

        # When the position is closed
        # looks for entry point
        if self.current_status == 'close':
            self.find_entry_point()

        else:
            try:
                # We check if we have to do something with the current position,
                # update current price highest price and
                # lowest price
                self.check_position()
            except Exception as error:
                logger.error("Unable to check position status : %s",error)

            current_effective_yield = self.effective_yield_calculation(
                self.current_price,
                self.open_price,
                settings.FEE,
            )

            # Give information about the program
            self.statistics['current_position_time'] = datetime.timedelta(
                seconds=round(time.time(), 0)
                - round(self.opening_time, 0)
            )
            self.statistics['open_price'] = self.open_price
            self.statistics['current_yield'] = current_effective_yield

    def find_entry_point(self):
        """[summary]

        Returns:
            [type]: [description]

        Yields:
            [type]: [description]
        """
        try:
            # Strong pump means buy decision
            if self.decision == "buy":
                if self.open_position():
                    return

        except Exception as error:
            logger.error('error while predicting : %s',error)

    def effective_yield_calculation(self,current_price, opening_price, fee):
        """Calculate the real yield considering fees and current price"""
        slope = float(current_price) / float(opening_price)
        fee = float(fee)
        return slope - (fee + (1 - fee) * slope * fee)

    def market_memory(self):
        """Should run in thread for market memory it updates the decision"""
        def metrics(trades:deque):
            """Gives volatilty for deque"""
            prices = [trade['last'] for trade in trades]
            return prices[-1]/prices[0]

        class History:
            """Class create to increase speed"""
            values = deque(maxlen=50000)

            def get_sorted_increased_history(self):
                """Give back the history with pump (value>1) in sorted list"""
                return sorted([value for value in self.values if value>1])

            def get_sorted_decreased_history(self):
                """Give back the history with dump (value<1) in sorted list"""
                return sorted([value for value in self.values if value<1])

            def get_highest_increase(self):
                """Give back the high fork (95% biggest) of the pump list"""
                history = self.get_sorted_increased_history()
                return history[int((len(history)-1)*0.95)]

            def get_highest_decrease(self):
                """Give back the high fork (95% biggest) of the dump list"""
                history = self.get_sorted_decreased_history()
                return history[int((len(history)-1)*0.05)]

        DATA_LENGTH = 20
        last_x_trades = deque(maxlen=DATA_LENGTH)
        history = History()

        # Initialize the first data
        while True:
            previous_data  = self.websocket.get_ticker(self.symbol).copy()
            if 'bid' in previous_data:
                # remove time metric
                previous_data.pop("time")
                break

        from __main__ import event
        logger.info("Successfuly started momentum analysis")
        while not event.is_set():
            current_data = self.websocket.get_ticker(self.symbol).copy()
            if 'bid' in current_data:
                # remove time metric
                current_data.pop("time")
                if previous_data.get("last") != current_data.get("last"):
                    last_x_trades.append(current_data)
                    previous_data = current_data
                    # fully loaded
                    if len(last_x_trades)==DATA_LENGTH:
                        metric = metrics(last_x_trades)
                        try:
                            # current positive gap is stronger the usual one => Strong buys
                            if metric > history.get_highest_increase() and len(history.values)>1000:
                                self.decision = "buy"
                            # current negative gap is stronger the usual one => Strong sells
                            elif metric < history.get_highest_decrease() and len(history.values)>1000:
                                self.decision = "sell"
                            else:
                                self.decision = "hodle"
                        except IndexError:
                            pass
                        history.values.append(metrics(last_x_trades))

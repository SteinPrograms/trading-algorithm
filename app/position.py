"""Module used for position management"""

import datetime
import time
import settings
from database import Database
from brokerconnection import RealCommands
from prediction import Prediction
from bot_exceptions import DatabaseException
from logs import logger

class Position:
    """This class is used to store all the data used to create orders and to make the calculation.
    Defaults : backtesting is True and symbol is 'BTC'
    """
    def __init__(self,*,backtesting : bool = True,symbol : str = 'BTC',database: Database):
        self.symbol = f'{symbol}/{settings.BASE_ASSET}'
        self.backtesting = backtesting
        self.status='close'
        self.current_effective_yield = 1
        self.highest_yield=1
        self.database = database
        self.identifier = None
        self.open_price = None
        self.current_price = None
        self.highest_price = None
        self.lowest_price = None
        self.opening_time = None
        self.effective_yield = None
        self.close_price = None
        self.close_mode = None
        self.expected_yield = None

    def is_open(self):
        """Return true if position is open"""
        return self.status=='open'

    def open_position(self):
        """This function send an open order to the broker, with the opening price,
        and then save the data inside the class Position.
        """
        if not self.backtesting:
            order = RealCommands().market_open(symbol=self.symbol, backtesting=self.backtesting)
            if order['error']:
                return False
            self.identifier = order['order']['id']
        else:
            # Simulation of opening position time by broker
            time.sleep(2)
        current_price = settings.broker.price(self.symbol)['ask']
        self.open_price = current_price
        self.current_price = current_price
        # Setting highest price and lowest price to the opening price
        self.highest_price = self.open_price
        self.lowest_price = self.open_price
        self.status = 'open'
        self.opening_time = time.time()
        return True


    def close_position(self):
        """This function send a close market order to the broker
        save the database inside the database
        """
        self.status = 'close'
        self.effective_yield = self.effective_yield_calculation(
                                    self.close_price,
                                    self.open_price,
                                    settings.FEE,
                                )
        if self.database.total_yield*self.effective_yield > self.highest_yield:
            self.highest_yield = self.database.total_yield*self.effective_yield

        try:
            order_data = RealCommands().get_order_status(self.identifier)
            self.database.add_position(data={
                'time':self.opening_time,
                'symbol':self.symbol,
                'yield':self.effective_yield,
                'walletValue':order_data.get('avgFillPrice',0)*order_data.get('filledSize',0),
            })
        except DatabaseException as error:
            print(error)


    def force_position_close(self):
        """Force position to close at marketprice"""
        if self.backtesting:
            self.close_price = self.current_price
        else:
            order = RealCommands().market_close(self.symbol, backtesting=self.backtesting)
            print(order)
            self.close_price = settings.broker.price(self.symbol)['ask']
        self.close_mode = "force-close"
        self.close_position()


    def check_position(self):
        """Update the current_price, the highest_price and the lowest price
        Then checks if it has to close the position
        """

        current_price = settings.broker.price(self.symbol)['bid']

        ## If the price is falling we have to lower the expected yield by the same ratio
        if self.current_price > current_price and self.expected_yield > 1 + settings.FEE * 2:
            self.expected_yield += current_price/self.current_price - 1

        self.current_price = current_price

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
        if self.current_effective_yield < settings.RISK:
            if self.backtesting:
                self.close_price = self.open_price * settings.RISK
            else:
                RealCommands().market_close(self.symbol, backtesting=self.backtesting)
                self.close_price = current_price
            self.close_mode = "stop-loss"
            self.close_position()
            return

        # Take profit on expected yield
        # Closing on take-profit :
        #   -> Check if the yield  is stronger  than the minimal yield considering fees and slippage
        if self.current_effective_yield > self.expected_yield:
            if self.backtesting:
                self.close_price = self.current_price
            else:
                RealCommands().market_close(symbol=self.symbol, backtesting=self.backtesting)
                self.close_price = current_price
            self.close_mode = "take-profit"
            self.close_position()
            return

    def manage_position(self):
        """Manage position : look for selling or buying actions"""

        statistics = {}

        # Update expected yield from the database
        try:
            self.expected_yield = self.database.levels._yield(self.symbol) - 2 * settings.FEE
        except DatabaseException as error:
            print(error)

        # When the position is closed
        # looks for entry point
        if self.status == 'close':
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
            statistics = {
                'current_price': self.current_price, 
                'open_price': self.open_price, 
                'highest_price': self.highest_price, 
                'lowest_price': self.lowest_price, 
                'position_yield': f'{str(round((current_effective_yield - 1) * 100, 2))} %',
                'current_position_time': str(datetime.timedelta(seconds=round(time.time(), 0) - round(self.opening_time, 0))),
                'expected_yield': self.expected_yield,
            }


        statistics['current_status'] = self.status
        statistics['total_yield'] = f'{str(round((self.database.total_yield - 1) * 100, 2))} %'

        for data, value__ in statistics.items():
            print(data, ':', value__, '\n')
        
        self.database.update_data(statistics)
        
    def find_entry_point(self):
        """[summary]

        Returns:
            [type]: [description]

        Yields:
            [type]: [description]
        """
        try:
            # We analyze the market with the signals defined inside prediction.py
            predict = Prediction(self.database).signal(self.symbol)

            for key,value in predict.items():
                print(key, ':', value, '\n')

            # If we get a buy signal then :
            if predict['signal'] == 'buy' and self.open_position():
                self.expected_yield = predict['yield']
                return

        except Exception as error:
            print(f'error while predicting : {error}')

    def effective_yield_calculation(self,current_price, opening_price, fee):
        r = float(current_price) / float(opening_price)
        f = float(fee)
        return r - (f + (1 - f) * r * f)

if __name__ == '__main__':
    position = Position(backtesting=False)
    position.open_position()
    position.force_position_close()

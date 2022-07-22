import settings
import numpy as np

from typing import Dict
from routine import Routine
from database import Database
from bot_exceptions import DataSizeException

class Prediction:
    """Class used to predict buy actions"""
    def __init__(self,database:Database):
        self.database = database
        self.drawdown = settings.DRAWDOWN

    def get_hourly_gap(self,):
        """Return gap"""
        self.database.retrieve_values()
        if len(hourly_values)>6:
            raise DataSizeException
        hourly_values = [30000,30202,30404]
        hourly_average = np.mean(hourly_values)
        return np.mean([np.pow(hourly_average-hourly_value,2)] for hourly_value in hourly_values)



    def signal(self,symbol:str):
        """Give the buy signal

        We buy if there is a 1% drop since the previous exit price
        On program start previous exit price = current price
        """
        with self.database.get_exit_price() as exit_price:
            if current_price/exit_price < 1-settings.EXPECTED_YIELD:
        return {'signal':'buy'}
        

if __name__ == "__main__":
    print(settings.broker.price("ETH/USD"))

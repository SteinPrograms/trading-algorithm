import settings
from database import Database


class Prediction:
    """Class used to predict buy actions"""
    def __init__(self,database:Database):
        self.database = database
        self.drawdown = settings.DRAWDOWN

    def signal(self,symbol:str):
        """Give the buy signal

        We buy if there is a 1% drop since the previous exit price
        On program start previous exit price = current price
        """
        return {'signal':'buy'}


if __name__ == "__main__":
    print(settings.broker.price("ETH/USD"))

import settings

from typing import Dict
from routine import Routine
from database import Database

class Prediction:
    """Class used to predict buy actions"""
    def __init__(self,database:Database):
        self.database = database
        self.drawdown = settings.DRAWDOWN

    async def signal(self,symbol:str) -> Dict[str]:
        """Give the buy signal"""
        current_price = settings.broker.price(symbol)["bid"]
        if round(current_price/100,0)==round(self.database.get_target_value(symbol)/100,0):
            return {"signal":"buy",
                    "yield":self.database.get_expected_yield(symbol) - 2 * settings.FEE,
                    }
        else:
            return {"signal":"neutral"}

if __name__ == "__main__":
    print(settings.broker.price("ETH/USD"))

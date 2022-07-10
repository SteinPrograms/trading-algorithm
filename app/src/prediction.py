import settings
    
from routine import Routine
from database import Database

def mean(array : list)->float:
    return sum(array)/len(array)


class Prediction:
    def __init__(self,database:Database):
        self.database = database
        settings.DRAWDOWN

    def fetch_levels(self,):
        pass

    def signal(self,symbol:str) ->dict[str]:
        current_price = settings.broker.price(symbol)["bid"]
        if round(current_price/100,0)==round(Database().get_target_value(symbol)/100,0):
            return {"signal":"buy",
                    "yield":Database().get_expected_yield(symbol) - 2 * settings.FEE,
                    }
        else:
            return {"signal":"neutral"}
        
        
if __name__ == "__main__":
    print(settings.broker.price("ETH/USD"))